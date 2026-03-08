from src.utils.ui import safe_click, wait_for
from src.locators.android.menu_locators import MenuLocators


class MenuComponent:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        safe_click(self.driver, MenuLocators.MENU_BTN, timeout=10)

    def logout(self):
        safe_click(self.driver, MenuLocators.LOGOUT_BTN, timeout=10)

    def logout_visible(self, timeout: int = 10) -> bool:
        try:
            wait_for(self.driver, MenuLocators.LOGOUT_BTN, timeout=timeout)
            return True
        except Exception:
            return False
