import pytest
from src.page_objects.products_page import ProductsPage


@pytest.mark.smoke
@pytest.mark.android
def test_add_to_cart(seed_standard_user_session):
    _, products = seed_standard_user_session

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE button after adding item to cart"


@pytest.mark.regression
@pytest.mark.android
def test_cart_icon_is_visible_on_products_screen(seed_standard_user_session):
    _, products = seed_standard_user_session

    assert products.cart_icon_visible(), "Expected cart icon on products screen"


@pytest.mark.regression
@pytest.mark.android
def test_add_and_remove_item_toggles_button_state(seed_standard_user_session):
    _, products = seed_standard_user_session

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE button after adding item"

    products.remove_first_item_from_cart()
    assert products.add_button_visible(), "Expected ADD TO CART button after removing item"


@pytest.mark.regression
@pytest.mark.android
def test_sort_control_is_visible_on_products_screen(seed_standard_user_session):
    _, products = seed_standard_user_session

    assert products.sort_button_visible(), "Expected sort selector on products screen"


@pytest.mark.regression
@pytest.mark.android
def test_products_show_titles_and_prices(seed_standard_user_session):
    _, products = seed_standard_user_session

    titles = products.item_titles()
    prices = products.item_prices()

    assert len(titles) >= 2, "Expected at least two visible product titles"
    assert len(prices) >= 2, "Expected at least two visible product prices"
    assert all(price > 0 for price in prices), "Expected positive product prices"


@pytest.mark.regression
@pytest.mark.android
def test_default_product_order_starts_with_backpack(seed_standard_user_session):
    _, products = seed_standard_user_session

    titles = products.item_titles()
    assert titles, "Expected at least one visible product title"
    assert titles[0] == "Sauce Labs Backpack", "Unexpected first product in default order"


@pytest.mark.regression
@pytest.mark.android
def test_visible_product_titles_are_unique(seed_standard_user_session):
    _, products = seed_standard_user_session

    titles = products.item_titles()
    assert titles, "Expected at least one visible product title"
    assert len(titles) == len(set(titles)), "Expected unique visible product titles"


@pytest.mark.regression
@pytest.mark.android
def test_visible_product_title_price_counts_match(seed_standard_user_session):
    _, products = seed_standard_user_session

    titles = products.item_titles()
    prices = products.item_prices()

    assert len(titles) >= 2, "Expected at least two visible product titles"
    assert len(prices) >= 2, "Expected at least two visible product prices"
    assert len(prices) <= len(titles), "Expected visible prices to be a subset of visible titles"


@pytest.mark.regression
@pytest.mark.android
def test_add_remove_cycle_is_repeatable(seed_standard_user_session):
    _, products = seed_standard_user_session

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE state after first add"
    products.remove_first_item_from_cart()
    assert products.add_button_visible(), "Expected ADD TO CART state after first remove"

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE state after second add"
    products.remove_first_item_from_cart()
    assert products.add_button_visible(), "Expected ADD TO CART state after second remove"


@pytest.mark.regression
@pytest.mark.android
def test_problem_user_can_add_item_to_cart(login_page, users_test_data):
    user = users_test_data["problem_user"]
    products = ProductsPage(login_page.driver)

    login_page.login(user["username"], user["password"])
    assert products.wait_until_loaded(), "Expected problem_user to reach products"

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected problem_user to add item to cart"
