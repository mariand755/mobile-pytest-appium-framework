from appium import webdriver
from appium.options.android import UiAutomator2Options
from urllib.parse import urlparse, urlunparse
import os

from src.config.settings import (
    RUN_ENV,
    APPIUM_SERVER_URL,
    ANDROID_LOCAL_APP_PATH,
    ANDROID_SAUCE_APP,
)

def _with_basic_auth(url: str, user: str, key: str) -> str:
    """
    If the URL doesn't already include auth, add https://user:key@host...
    """
    parsed = urlparse(url)

    # Already has username/password in URL → return as-is
    if parsed.username or ("@" in parsed.netloc):
        return url

    netloc = f"{user}:{key}@{parsed.netloc}"
    return urlunparse(parsed._replace(netloc=netloc))

def _get_remote_url() -> str:
    """
    CI: force Sauce basic auth into URL (if not already present)
    Local: return as-is
    """
    url = APPIUM_SERVER_URL
    if RUN_ENV == "ci":
        user = os.getenv("SAUCE_USERNAME", "")
        key = os.getenv("SAUCE_ACCESS_KEY", "")
        if user and key:
            url = _with_basic_auth(url, user, key)
    return url


def create_android_driver():
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"

    # App selection (local vs sauce)
    if RUN_ENV == "ci":
        opts.app = ANDROID_SAUCE_APP

        # IMPORTANT: Sauce usually needs a supported deviceName + platformVersion
        # Prefer controlling these via env vars so you can tweak without code changes.
        opts.device_name = os.getenv(
            "SAUCE_ANDROID_DEVICE",
            "Android GoogleAPI Emulator"
        )
        opts.platform_version = os.getenv(
            "SAUCE_ANDROID_PLATFORM_VERSION",
            "14.0"
        )

        # Optional but helpful metadata (shows up in Sauce UI)
        opts.set_capability("sauce:options", {
            "name": os.getenv("SAUCE_TEST_NAME", "Android - Smoke"),
            "build": os.getenv("GITHUB_RUN_NUMBER", "local"),
        })

    else:
        # Local docker only
        opts.device_name = "Android Emulator"
        opts.udid = "host.docker.internal:5555"
        opts.app = ANDROID_LOCAL_APP_PATH

    # App launch tuning (Sauce sample app)
    opts.app_package = "com.swaglabsmobileapp"
    opts.app_activity = ".MainActivity"
    opts.app_wait_activity = "*"
    opts.app_wait_duration = 60000

    # Stability
    opts.new_command_timeout = 180
    opts.no_reset = False
    opts.full_reset = True
    opts.auto_grant_permissions = True

    remote_url = _get_remote_url()
    return webdriver.Remote(command_executor=remote_url, options=opts)
