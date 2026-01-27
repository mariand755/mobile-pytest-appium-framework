import pytest
from src.page_objects.login_page import LoginPage
from src.page_objects.products_page import ProductsPage

@pytest.mark.smoke
@pytest.mark.android
def test_add_to_cart(driver):
    login = LoginPage(driver)
    products = ProductsPage(driver)

    login.login_as_standard_user()
    products.wait_until_loaded()

    products.add_first_item_to_cart()
    assert products.added_to_cart(), "Expected REMOVE button after adding item to cart"

