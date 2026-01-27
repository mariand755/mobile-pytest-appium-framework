from src.utils.ui import find, safe_click, wait_for
from src.locators.android.login_locators import LoginLocators


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def wait_until_loaded(self, timeout: int = 10):
        wait_for(self.driver, LoginLocators.LOGIN_BTN, timeout=timeout)
        return self

    def login(self, username: str, password: str):
        # ensure we're on the login screen
        self.wait_until_loaded()

        # clear to avoid leftovers if a previous run left text behind
        user_el = find(self.driver, LoginLocators.USERNAME)
        user_el.clear()
        user_el.send_keys(username)

        pass_el = find(self.driver, LoginLocators.PASSWORD)
        pass_el.clear()
        pass_el.send_keys(password)

        safe_click(self.driver, LoginLocators.LOGIN_BTN, timeout=10)

    def login_as_standard_user(self):
        self.login("standard_user", "secret_sauce")

    def login_as_locked_out_user(self):
        self.login("locked_out_user", "secret_sauce")

    def is_loaded(self) -> bool:
        try:
            self.wait_until_loaded(timeout=10)
            return True
        except Exception:
            return False

    def error_displayed(self) -> bool:
        return find(self.driver, LoginLocators.ERROR_TEXT).is_displayed()

    def get_error_text(self) -> str:
        return find(self.driver, LoginLocators.ERROR_TEXT).text.strip()
