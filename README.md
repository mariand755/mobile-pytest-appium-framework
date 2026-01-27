# 📱 Mobile Test Automation Framework

> A Docker-first mobile test automation framework built with **Pytest** + **Appium**, 
designed for local Android development and Sauce Labs execution with CI/CD support.


This project demonstrates how modern mobile QE teams build scalable, portable, and CI-ready test platforms with **zero local dependencies** beyond Docker.

---

## 🎯 Key Features

- ✅ **Docker-First Architecture** – Run tests anywhere Docker is available
- ✅ **Pytest Best Practices** – Fixtures, markers, parameterization, and driver factory patterns
- ✅ **Multi-Platform Ready** – Android and iOS support
- ✅ **Cloud-Native** – Seamless local emulator ↔ Sauce Labs parity
- ✅ **CI/CD Integration** – GitHub Actions workflows included
- ✅ **Allure Reporting** – Rich test reports with screenshots and logs
- ✅ **Production-Ready** – Real-world structure, error handling, and best practices

**If Docker runs, tests run.** No local Python, Node, Java, or Android SDK installs required.

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
- **Smoke test suite** – Login, invalid login, logout, add-to-cart
- **Page Object Model** – Screens + reusable components
- **Locator abstraction** – Platform-specific locator files
- **UI helpers** – Safe clicks, waits, reusable finders

---

## ✅ Prerequisites

- **Docker** + **Docker Compose**
- **Android Emulator** running (Android Studio is fine)

---

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
docker compose -f docker/compose.local.android.yml run --rm tests -- pytest -q
```

### Run Tests by Marker

```bash
docker compose -f docker/compose.local.android.yml run --rm tests -- pytest -m "smoke and android" -q
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
| `smoke` | Fast validation |
| `android` | Android-only tests |
| `ios` | iOS-only tests (reserved for future) |

---

## ⚙️ Configuration

### Environment Setup

Copy the environment template:

```bash
cp .env.example .env
```

### Key Environment Variables

| Variable | Description |
|----------|-------------|
| `APPIUM_SERVER_URL` | Defaults to Appium container |
| `ANDROID_APP_PATH` | Path inside container; default uses `/work/...` |
| `SAUCE_USERNAME` | Sauce Labs username (optional) |
| `SAUCE_ACCESS_KEY` | Sauce Labs access key (optional) |

---

## 📂 Project Structure

```
.
├── .github/workflows/              # CI workflows
├── apps/                           # App binaries (ignored; keep local)
│   ├── android/
│   └── ios/
├── docker/
│   ├── appium/                     # Appium image + start script
│   ├── Dockerfile                  # Test runner image
│   ├── compose.local.android.yml   # Android Compose override
│   └── entrypoint.sh               # Entrypoint script
├── scripts/                        # Helper utilities
│   └── download_app.sh             # App download script
├── src/
├── conftest.py                     # Pytest fixtures
├── core/
│   └── driver_factory.py           # Driver setup
├── page_objects/                   # Screen & component abstractions
├── locators/                       # Platform-specific locators
├── utils/                          # UI helpers (waits, safe clicks)
└── tests/
    └── smoke/                      # Smoke tests

├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔄 CI/CD Workflows
The PR smoke workflow runs Android smoke tests against Sauce Labs 
and blocks merges if failures occur.

Workflows are located in `.github/workflows/`:

- **`pr-smoke.yml`** – PR smoke gate
- **`manual-run.yml`** – Manual trigger workflow

---

## 📝 Notes
- Local Android execution uses a host emulator connected via ADB over TCP
- **APK/IPA binaries** should stay local (repo uses `.gitkeep` in `apps/`)
- **Allure reporting** is ready to wire (results directory lives under `reports/`)
