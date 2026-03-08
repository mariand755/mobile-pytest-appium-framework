from src.utils.ui import find, safe_click, wait_for
from src.locators.android.products_locators import ProductsLocators


class ProductsPage:
    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self, timeout: int = 10):
        wait_for(self.driver, ProductsLocators.TITLE, timeout=timeout)
        return self

    def add_first_item_to_cart(self):
        safe_click(self.driver, ProductsLocators.ADD_TO_CART_BTN, timeout=10)

    def remove_first_item_from_cart(self):
        safe_click(self.driver, ProductsLocators.REMOVE_BTN, timeout=10)

    def added_to_cart(self, timeout: int = 10) -> bool:
        try:
            wait_for(self.driver, ProductsLocators.REMOVE_BTN, timeout=timeout)
            return True
        except Exception:
            return False

    def add_button_visible(self, timeout: int = 10) -> bool:
        try:
            wait_for(self.driver, ProductsLocators.ADD_TO_CART_BTN, timeout=timeout)
            return True
        except Exception:
            return False

    def cart_icon_visible(self, timeout: int = 10) -> bool:
        try:
            wait_for(self.driver, ProductsLocators.CART_ICON, timeout=timeout)
            return True
        except Exception:
            return False
