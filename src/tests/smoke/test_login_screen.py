import pytest
from src.page_objects.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.android
def test_login_screen_loaded(driver):
    login = LoginPage(driver)
    assert login.is_loaded(), "Login screen did not load on app launch"
