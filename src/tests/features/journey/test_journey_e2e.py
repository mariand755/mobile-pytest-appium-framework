import pytest
from src.page_objects.products_page import ProductsPage
from src.page_objects.menu_component import MenuComponent


@pytest.mark.e2e
@pytest.mark.android
def test_end_to_end_login_add_to_cart_logout(seed_cart_with_item):
    login, products = seed_cart_with_item
    menu = MenuComponent(login.driver)

    assert products.added_to_cart(), "Expected REMOVE state after adding item"

    menu.open()
    menu.logout()
    assert login.is_loaded(), "Expected user to return to login screen after logout"


@pytest.mark.e2e
@pytest.mark.android
def test_invalid_login_then_valid_login_flow(login_page, users_test_data):
    products = ProductsPage(login_page.driver)

    login_page.login("invalid_user", "wrong_password")
    assert "do not match" in login_page.get_error_text().lower()

    user = users_test_data["standard_user"]
    login_page.login(user["username"], user["password"])
    assert products.wait_until_loaded(), "Expected successful login after valid credentials"
