from appium.webdriver.common.appiumby import AppiumBy


class ProductsLocators:
    TITLE = (AppiumBy.ACCESSIBILITY_ID, "test-PRODUCTS")
    SORT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-Modal Selector Button")
    ITEM_TITLE = (AppiumBy.ACCESSIBILITY_ID, "test-Item title")
    ITEM_PRICE = (AppiumBy.ACCESSIBILITY_ID, "test-Price")

    ADD_TO_CART_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-ADD TO CART")
    REMOVE_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-REMOVE")

    CART_ICON = (AppiumBy.ACCESSIBILITY_ID, "test-Cart")
