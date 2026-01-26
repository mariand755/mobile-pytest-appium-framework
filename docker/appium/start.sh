#!/usr/bin/env bash
set -euo pipefail

# Where Docker can reach your host emulator (Mac/Windows)
HOST_ADB_TARGET="${HOST_ADB_TARGET:-host.docker.internal:5555}"

echo "Waiting for ADB target: ${HOST_ADB_TARGET}"

# Try to connect until emulator is reachable
until adb connect "${HOST_ADB_TARGET}" | grep -q "connected\|already connected"; do
  echo "ADB not ready yet. Retrying in 2s..."
  sleep 2
done

echo "ADB connected. Current devices:"
adb devices || true

# Start Appium
# Use /wd/hub base-path for compatibility with older client defaults
exec appium --address 0.0.0.0 --port 4723 --base-path /wd/hub --log-level info
