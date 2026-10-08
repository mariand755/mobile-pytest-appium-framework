#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ci_retry_pytest.sh \
    --compose-file <path> \
    --env-file <path> \
    --markers "<pytest -m expression>" \
    [--allure-dir <path>] \
    [--service <docker compose service>] \
    [--per-test-reruns <n>] \
    [--per-test-reruns-delay-seconds <n>] \
    [--max-retries <n>] \
    [--retry-delay-seconds <n>]

Example:
  ci_retry_pytest.sh \
    --compose-file docker/compose.yml \
    --env-file .env \
    --markers "smoke and android" \
    --allure-dir reports/allure-results \
    --per-test-reruns 1 \
    --per-test-reruns-delay-seconds 5 \
    --max-retries 1 \
    --retry-delay-seconds 10
EOF
}

COMPOSE_FILE=""
ENV_FILE=""
MARKERS=""
ALLURE_DIR="reports/allure-results"
SERVICE="tests"
PER_TEST_RERUNS=0
PER_TEST_RERUNS_DELAY_SECONDS=0
MAX_RETRIES=1
RETRY_DELAY_SECONDS=10

while [[ $# -gt 0 ]]; do
  case "$1" in
    --compose-file)
      COMPOSE_FILE="$2"
      shift 2
      ;;
    --env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    --markers)
      MARKERS="$2"
      shift 2
      ;;
    --allure-dir)
      ALLURE_DIR="$2"
      shift 2
      ;;
    --service)
      SERVICE="$2"
      shift 2
      ;;
    --per-test-reruns)
      PER_TEST_RERUNS="$2"
      shift 2
      ;;
    --per-test-reruns-delay-seconds)
      PER_TEST_RERUNS_DELAY_SECONDS="$2"
      shift 2
      ;;
    --max-retries)
      MAX_RETRIES="$2"
      shift 2
      ;;
    --retry-delay-seconds)
      RETRY_DELAY_SECONDS="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$COMPOSE_FILE" || -z "$ENV_FILE" || -z "$MARKERS" ]]; then
  echo "Missing required arguments." >&2
  usage
  exit 2
fi

if ! [[ "$MAX_RETRIES" =~ ^[0-9]+$ ]]; then
  echo "--max-retries must be a non-negative integer." >&2
  exit 2
fi

if ! [[ "$PER_TEST_RERUNS" =~ ^[0-9]+$ ]]; then
  echo "--per-test-reruns must be a non-negative integer." >&2
  exit 2
fi

if ! [[ "$PER_TEST_RERUNS_DELAY_SECONDS" =~ ^[0-9]+$ ]]; then
  echo "--per-test-reruns-delay-seconds must be a non-negative integer." >&2
  exit 2
fi

if ! [[ "$RETRY_DELAY_SECONDS" =~ ^[0-9]+$ ]]; then
  echo "--retry-delay-seconds must be a non-negative integer." >&2
  exit 2
fi

mkdir -p reports/artifacts
mkdir -p "$ALLURE_DIR"

LOG_DIR="reports/artifacts/retry-logs"
mkdir -p "$LOG_DIR"

# Retry only likely infrastructure/transient failures, not product/account issues.
is_transient_failure() {
  local log_file="$1"
  local transient_pattern
  local non_retry_pattern

  transient_pattern="SessionNotCreatedException|New Session request failed|Could not start a new session|Max retries exceeded|ECONNRESET|ETIMEDOUT|TimeoutException|timed out|Read timed out|Connection refused|Connection reset|ProxyError|socket hang up|502 Bad Gateway|503 Service Unavailable|504 Gateway Timeout|Temporary failure in name resolution"

  non_retry_pattern="run out of minutes|purchase a subscription|authentication failed|invalid credentials|one or more Sauce secrets are missing|Skipped: set ENABLE_"

  if grep -Eqi "$non_retry_pattern" "$log_file"; then
    return 1
  fi

  grep -Eqi "$transient_pattern" "$log_file"
}

attempt=1
max_attempts=$((MAX_RETRIES + 1))
last_exit=1

while [[ "$attempt" -le "$max_attempts" ]]; do
  log_file="$LOG_DIR/pytest_attempt_${attempt}.log"
  echo "=== Pytest attempt ${attempt}/${max_attempts} ==="

  pytest_cmd=(pytest -m "$MARKERS" -q --alluredir="$ALLURE_DIR")

  if [[ "$PER_TEST_RERUNS" -gt 0 ]]; then
    pytest_cmd+=(--reruns "$PER_TEST_RERUNS")

    if [[ "$PER_TEST_RERUNS_DELAY_SECONDS" -gt 0 ]]; then
      pytest_cmd+=(--reruns-delay "$PER_TEST_RERUNS_DELAY_SECONDS")
    fi
  fi

  echo "Per-test reruns: ${PER_TEST_RERUNS}, per-test delay: ${PER_TEST_RERUNS_DELAY_SECONDS}s"

  set +e
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" run --rm "$SERVICE" \
    "${pytest_cmd[@]}" 2>&1 | tee "$log_file"
  cmd_exit=${PIPESTATUS[0]}
  set -e

  if [[ "$cmd_exit" -eq 0 ]]; then
    echo "Attempt ${attempt} succeeded."
    exit 0
  fi

  last_exit="$cmd_exit"

  if [[ "$attempt" -gt "$MAX_RETRIES" ]]; then
    echo "No retries left; exiting with code ${cmd_exit}."
    break
  fi

  if ! is_transient_failure "$log_file"; then
    echo "Failure does not match transient retry policy; exiting with code ${cmd_exit}."
    break
  fi

  next_attempt=$((attempt + 1))
  echo "Transient failure detected. Retrying in ${RETRY_DELAY_SECONDS}s (attempt ${next_attempt}/${max_attempts})..."

  rm -rf "$ALLURE_DIR"
  mkdir -p "$ALLURE_DIR"
  find reports/artifacts -maxdepth 1 -type f \( -name '*.png' -o -name '*.xml' \) -delete || true

  sleep "$RETRY_DELAY_SECONDS"
  attempt="$next_attempt"
done

exit "$last_exit"
