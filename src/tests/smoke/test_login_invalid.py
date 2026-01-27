import pytest
from src.page_objects.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.android
def test_invalid_login(driver):
    login = LoginPage(driver)
    login.login("invalid_user", "wrong_password")

    assert "do not match" in login.get_error_text().lower()

