# 📱 Mobile Test Automation Framework

> A Docker-first mobile test automation framework built with **Pytest** + **Appium**, 
designed for local Android development and Sauce Labs execution with CI/CD support.


This project demonstrates how modern mobile QE teams build scalable, portable, and CI-ready test platforms with Docker-managed dependencies.
For local Android runs, you still need a running emulator and `adb` access on the host.

---

## 🎯 Key Features

- ✅ **Docker-First Architecture** – Run tests anywhere Docker is available
- ✅ **Pytest Best Practices** – Fixtures, markers, parameterization, and driver factory patterns
- ✅ **Multi-Platform Ready** – Android and iOS support
- ✅ **Cloud-Native** – Seamless local emulator ↔ Sauce Labs parity
- ✅ **CI/CD Integration** – GitHub Actions workflows included
- ✅ **Allure Reporting** – Rich test reports with screenshots and logs
- ✅ **Production-Ready** – Real-world structure, error handling, and best practices

**If Docker runs, tests run.** No local Python or Node setup is required.

---

## 📋 Table of Contents

- [What's in Here](#-whats-in-here)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Test Organization](#-test-organization)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [CI/CD Workflows](#-cicd-workflows)
- [Notes](#-notes)

---

## 📦 What's in Here

- **Appium 2 + UiAutomator2** – Running in a dedicated container
- **Pytest runner** – Isolated in a separate container
- **Android emulator** – Runs on the host, connected via ADB over TCP
- **Feature-based test suites** – Auth, catalog, navigation, and journey flows
- **Marker-driven execution** – `smoke`, `regression`, `e2e`, plus platform markers
- **Page Object Model** – Screens + reusable components
- **Locator abstraction** – Platform-specific locator files
- **Data-driven coverage** – JSON and CSV test data inputs
- **Deterministic test setup** – Clean-state fixtures and UI seeding helpers
- **UI helpers** – Safe clicks, waits, reusable finders

---

## ✅ Prerequisites

- **Docker** + **Docker Compose**
- **Android Emulator** running (Android Studio is fine)

---

## 🧪 Local vs CI Execution

This framework supports running tests both locally (Docker + local APK)
and in CI (GitHub Actions + Sauce Labs).

### Local (Docker + Emulator)
- Uses a locally mounted APK
- Default behavior when `RUN_ENV=local` (default)
- Compose files live under `docker/`; run commands from repo root and always pass `-f docker/...`.

```bash
docker compose -f docker/compose.local.android.yml run --rm tests \
  -- pytest -m "smoke and android"
```

## 🚀 Quick Start

### Setup (Local Android)

1. **Start emulator + enable ADB over TCP on host**

```bash
adb devices
adb -s emulator-5554 tcpip 5555
```

2. **Bring up Appium server (Docker)**

```bash
docker compose -f docker/compose.local.android.yml up -d
```

3. **Run smoke test (Docker)**

```bash
docker compose -f docker/compose.local.android.yml run --rm tests -- \
  pytest -m "smoke and android" -q
```

### Run Tests by Marker

```bash
docker compose -f docker/compose.local.android.yml run --rm tests -- pytest -m "smoke and android" -q
docker compose -f docker/compose.local.android.yml run --rm tests -- pytest -m "regression and android" -q
docker compose -f docker/compose.local.android.yml run --rm tests -- pytest -m "e2e and android" -q
```

### Stop Services

```bash
docker compose -f docker/compose.local.android.yml down
```

---

## 🏷️ Test Organization (Pytest Markers)

Markers are defined in `pytest.ini`:

| Marker | Purpose |
|--------|----------|
| `smoke` | Fast critical-path validation |
| `regression` | Broader feature coverage |
| `e2e` | Cross-feature journey coverage |
| `android` | Android-targeted tests |
| `ios` | iOS-targeted tests |
| `sauce` | Tests intended for Sauce Labs execution |

---

## ⚙️ Configuration

### Environment Setup

Copy the environment template:

```bash
cp .env.example .env.local
# Optional for CI compose usage:
# cp .env.example .env
```

### Key Environment Variables

| Variable | Description |
|----------|-------------|
| `RUN_ENV` | `local` or `ci` |
| `PLATFORM` | `android` or `ios` |
| `APPIUM_SERVER_URL` | Appium server endpoint |
| `ANDROID_LOCAL_APP_PATH` | Local APK path (Docker container) |
| `ANDROID_SAUCE_APP` | Sauce Storage APK reference |
| `IOS_SAUCE_APP` | Sauce Storage iOS app reference (`.zip`) |
| `SAUCE_USERNAME` | Sauce Labs username |
| `SAUCE_ACCESS_KEY` | Sauce Labs access key |
| `SAUCE_REGION` | Sauce Labs region (for example `us-west-1`) |
| `SAUCE_ANDROID_DEVICE` | Android device/emulator name for Sauce |
| `SAUCE_ANDROID_PLATFORM_VERSION` | Android platform version for Sauce |

---


## 📂 Project Structure

```
.
├── .github/workflows/              # CI workflows
│   ├── manual-run.yml
│   ├── pre-release-full-run.yml
│   ├── pr-mobile-gate.yml
│   └── weekly-regression.yml
├── apps/                           # App binaries (ignored; keep local)
│   ├── android/
│   └── ios/
├── docker/
│   ├── appium/                     # Appium image + start script
│   ├── Dockerfile                  # Test runner image
│   ├── compose.local.android.yml   # Android Compose override
│   ├── compose.yml                 # CI/Sauce compose file
│   └── entrypoint.sh               # Entrypoint script
├── reports/
│   ├── allure-results/
│   └── artifacts/
├── scripts/                        # Helper utilities
│   └── download_app.sh             # App download script
├── src/
│   ├── config/
│   │   ├── capabilities/
│   │   ├── environments/
│   │   ├── test_data/
│   │   └── settings.py
│   ├── core/
│   │   └── driver_factory.py       # Driver setup
│   ├── locators/
│   │   ├── android/
│   │   └── ios/
│   ├── page_objects/               # Screen & component abstractions
│   │   ├── login_page.py
│   │   ├── menu_component.py
│   │   └── products_page.py
│   ├── tests/
│   │   └── features/
│   │       ├── auth/test_login.py
│   │       ├── catalog/test_product.py
│   │       ├── journey/test_journey_e2e.py
│   │       └── navigation/test_navigation.py
│   ├── utils/
│   │   └── ui.py
│   └── conftest.py                 # Fixtures + test lifecycle hooks
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔄 CI/CD Workflows
The workflows run tests in Docker and upload Allure/failure artifacts.

Workflows are located in `.github/workflows/`:

- **`pr-mobile-gate.yml`** – Pull request mobile gate on `main` (currently runs Android smoke checks in Sauce)
- **`manual-run.yml`** – Manual Sauce run with selectable `platform` and marker expression
- **`weekly-regression.yml`** – Scheduled + manual Android regression run (`pytest -m "regression and android"`)
- **`pre-release-full-run.yml`** – Manual Android pre-release run (`pytest -m "(smoke or regression or e2e) and android"`)

---

## 📝 Notes
- Local Android execution uses a host emulator connected via ADB over TCP
- **APK/IPA binaries** should stay local (repo uses `.gitkeep` in `apps/`)
- **Allure reporting** is ready to wire (results directory lives under `reports/`)
