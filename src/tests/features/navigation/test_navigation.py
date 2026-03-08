import pytest
from src.page_objects.menu_component import MenuComponent


@pytest.mark.smoke
@pytest.mark.android
def test_logout(seed_standard_user_session):
    login, _ = seed_standard_user_session
    menu = MenuComponent(login.driver)

    menu.open()
    menu.logout()

    assert login.is_loaded()


@pytest.mark.regression
@pytest.mark.android
def test_menu_open_displays_logout_action(seed_standard_user_session):
    login, _ = seed_standard_user_session
    menu = MenuComponent(login.driver)

    menu.open()
    assert menu.logout_visible(), "Expected LOGOUT action in opened menu"
