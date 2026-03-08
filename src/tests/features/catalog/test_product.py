import pytest


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
