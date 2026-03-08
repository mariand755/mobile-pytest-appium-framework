import pytest


@pytest.mark.smoke
@pytest.mark.android
def test_login_screen_loaded(login_page):
    assert login_page.is_loaded(), "Login screen did not load on app launch"


@pytest.mark.smoke
@pytest.mark.android
def test_invalid_login(login_page, invalid_login_case):
    login_page.login(
        invalid_login_case["username"],
        invalid_login_case["password"],
    )

    expected = invalid_login_case["expected_error_contains"].lower()
    assert expected in login_page.get_error_text().lower()


@pytest.mark.regression
@pytest.mark.android
def test_standard_user_can_login_from_users_data(seed_standard_user_session):
    _, products = seed_standard_user_session
    assert products.wait_until_loaded()


@pytest.mark.regression
@pytest.mark.android
def test_locked_out_user_sees_expected_error(login_page, users_test_data):
    user = users_test_data["locked_out_user"]
    login_page.login(user["username"], user["password"])

    assert "locked out" in login_page.get_error_text().lower()
