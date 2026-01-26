from appium import webdriver
from appium.options.android import UiAutomator2Options
from src.config.settings import APPIUM_SERVER_URL, ANDROID_APP_PATH

def create_android_driver():
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = "Android Emulator"

    # ADB over TCP target
    opts.udid = "host.docker.internal:5555"

    # App under test
    opts.app = ANDROID_APP_PATH

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

    return webdriver.Remote(command_executor=APPIUM_SERVER_URL, options=opts)
