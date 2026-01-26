import pytest

pytestmark = [pytest.mark.smoke, pytest.mark.android]

def test_launch_app(driver):
    # simple proof test: App opened and session exists
    assert driver.session_id is not None
