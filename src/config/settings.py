import os

def get_env(name: str, default: str | None = None) -> str:
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

APPIUM_SERVER_URL = get_env("APPIUM_SERVER_URL", "http://localhost:4723/wd/hub")
PLATFORM = get_env("PLATFORM", "android").lower()

ANDROID_APP_PATH = os.getenv("ANDROID_APP_PATH", "")  # local run
