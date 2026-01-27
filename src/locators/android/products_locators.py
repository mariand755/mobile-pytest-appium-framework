from appium.webdriver.common.appiumby import AppiumBy


class ProductsLocators:
    TITLE = (AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS")

    ADD_TO_CART_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART")
    REMOVE_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")

    CART_ICON = (AppiumBy.ACCESSIBILITY_ID, "test-Cart")
