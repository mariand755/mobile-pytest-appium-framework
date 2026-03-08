from appium import webdriver
from appium.options.android import UiAutomator2Options
from urllib.parse import urlparse, urlunparse
import os
import yaml

from src.config.settings import (
    RUN_ENV,
    APPIUM_SERVER_URL,
    CAPABILITIES_DIR,
    ANDROID_LOCAL_APP_PATH,
    ANDROID_SAUCE_APP,
)


def _load_yaml_dict(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise RuntimeError(f"Missing capabilities file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise RuntimeError(f"Capabilities file must contain a mapping: {file_path}")

    return data


def _android_capabilities_file() -> str:
    name = "android_sauce.yaml" if RUN_ENV == "ci" else "android_local.yaml"
    return os.path.join(CAPABILITIES_DIR, name)


def _build_android_options() -> UiAutomator2Options:
    caps = _load_yaml_dict(_android_capabilities_file())
    sauce_options = caps.pop("sauce_options", {})

    opts = UiAutomator2Options()

    for key, value in caps.items():
        if hasattr(opts, key):
            setattr(opts, key, value)
        else:
            opts.set_capability(key, value)

    # Keep env overrides so CI/local behavior is easy to tune without code edits.
    if RUN_ENV == "ci":
        opts.app = os.getenv("ANDROID_SAUCE_APP", ANDROID_SAUCE_APP)
        opts.device_name = os.getenv(
            "SAUCE_ANDROID_DEVICE",
            getattr(opts, "device_name", "Android GoogleAPI Emulator")
        )
        opts.platform_version = os.getenv(
            "SAUCE_ANDROID_PLATFORM_VERSION",
            getattr(opts, "platform_version", "14.0")
        )

        sauce_options = sauce_options if isinstance(sauce_options, dict) else {}
        sauce_options.update({
            "name": os.getenv("SAUCE_TEST_NAME", sauce_options.get("name", "Android - Smoke")),
            "build": os.getenv("GITHUB_RUN_NUMBER", sauce_options.get("build", "local")),
        })
        opts.set_capability("sauce:options", sauce_options)
    else:
        opts.app = os.getenv("ANDROID_LOCAL_APP_PATH", ANDROID_LOCAL_APP_PATH)

    return opts

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
    opts = _build_android_options()

    remote_url = _get_remote_url()
    return webdriver.Remote(command_executor=remote_url, options=opts)
