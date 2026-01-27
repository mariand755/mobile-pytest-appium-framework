import pytest
from src.page_objects.login_page import LoginPage
from src.page_objects.products_page import ProductsPage
from src.page_objects.menu_component import MenuComponent

@pytest.mark.smoke
@pytest.mark.android
def test_logout(driver):
    login = LoginPage(driver)
    products = ProductsPage(driver)
    menu = MenuComponent(driver)

    login.login_as_standard_user()
    products.wait_until_loaded()

    menu.open()
    menu.logout()

    assert login.is_loaded()
