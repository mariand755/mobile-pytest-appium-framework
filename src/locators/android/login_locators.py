from appium.webdriver.common.appiumby import AppiumBy

class LoginLocators:
    USERNAME = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    ERROR_TEXT = (
        AppiumBy.XPATH,
        "//*[@content-desc='test-Error message']//*[contains(@class,'TextView')]",
    )
