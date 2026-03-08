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


@pytest.mark.e2e
@pytest.mark.android
def test_locked_out_attempt_then_recovery_login(seed_standard_user_session, users_test_data):
    login, products = seed_standard_user_session
    menu = MenuComponent(login.driver)

    # Complete one authenticated action before forcing a full logout/login cycle.
    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected item to be in cart before logout"

    menu.open()
    menu.logout()
    assert login.is_loaded(), "Expected login screen after logout"

    locked_user = users_test_data["locked_out_user"]
    login.login(locked_user["username"], locked_user["password"])
    assert "locked out" in login.get_error_text().lower(), "Expected locked out error"

    standard_user = users_test_data["standard_user"]
    login.login(standard_user["username"], standard_user["password"])
    assert products.wait_until_loaded(), "Expected recovery login to reach products"


@pytest.mark.e2e
@pytest.mark.android
def test_standard_user_round_trip_session(seed_standard_user_session, users_test_data):
    login, products = seed_standard_user_session
    menu = MenuComponent(login.driver)

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE state after add"

    products.remove_first_item_from_cart()
    assert products.add_button_visible(), "Expected ADD TO CART after remove"

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE state after second add"

    menu.open()
    menu.logout()
    assert login.is_loaded(), "Expected login screen after logout"

    user = users_test_data["standard_user"]
    login.login(user["username"], user["password"])
    assert products.wait_until_loaded(), "Expected successful re-login to products"


@pytest.mark.e2e
@pytest.mark.android
def test_menu_access_requires_successful_auth(login_page, users_test_data):
    products = ProductsPage(login_page.driver)
    menu = MenuComponent(login_page.driver)

    # Negative path: menu should not be available before authentication.
    assert not menu.menu_button_visible(timeout=2), "Menu should not be visible pre-auth"

    login_page.login("invalid_user", "wrong_password")
    assert login_page.error_displayed(), "Expected invalid credential error"
    assert not menu.menu_button_visible(timeout=2), "Menu should still be hidden after failed login"

    user = users_test_data["standard_user"]
    login_page.login(user["username"], user["password"])
    assert products.wait_until_loaded(), "Expected successful login to products"
    assert menu.menu_button_visible(timeout=5), "Menu should be visible after successful auth"
