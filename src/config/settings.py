import os

def get_env(name: str, default: str | None = None) -> str:
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

# -------------------------
# Execution context
# -------------------------
RUN_ENV = os.getenv("RUN_ENV", "local").lower()  # local | ci
PLATFORM = os.getenv("PLATFORM", "android").lower()

# -------------------------
# Appium
# -------------------------
APPIUM_SERVER_URL = os.getenv(
    "APPIUM_SERVER_URL",
    "http://appium:4723/wd/hub"
)

# -------------------------
# Android app sources
# -------------------------
ANDROID_LOCAL_APP_PATH = os.getenv(
    "ANDROID_LOCAL_APP_PATH",
    "/apps/android/Android.SauceLabs.apk"
)

ANDROID_SAUCE_APP = os.getenv(
    "ANDROID_SAUCE_APP",
    "sauce-storage:Android.SauceLabs.apk"
)
