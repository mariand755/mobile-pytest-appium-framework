from appium.webdriver.common.appiumby import AppiumBy

class LoginLocators:
    USERNAME = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    ERROR_TEXT = (AppiumBy.XPATH, "//*[contains(@text,'Username and password do not match')]")
