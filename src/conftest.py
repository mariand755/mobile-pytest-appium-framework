import os
import csv
import json
import pytest
from datetime import datetime, timezone
from pathlib import Path
from src.core.driver_factory import create_android_driver
from src.page_objects.login_page import LoginPage
from src.page_objects.products_page import ProductsPage


TEST_DATA_DIR = Path(__file__).parent / "config" / "test_data"


def _read_csv_test_data(file_name: str) -> list[dict]:
    file_path = TEST_DATA_DIR / file_name
    if not file_path.exists():
        raise RuntimeError(f"Missing test data file: {file_path}")

    with file_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def _read_json_test_data(file_name: str) -> dict:
    file_path = TEST_DATA_DIR / file_name
    if not file_path.exists():
        raise RuntimeError(f"Missing test data file: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise RuntimeError(f"Expected JSON object in: {file_path}")

    return data


def _wait_for_login_screen(driver, timeout: int = 30, attempts: int = 2) -> LoginPage:
    page = LoginPage(driver)
    last_error: Exception | None = None

    for _ in range(attempts):
        try:
            page.wait_until_loaded(timeout=timeout)
            return page
        except Exception as exc:
            last_error = exc

    if last_error is not None:
        raise last_error

    return page


@pytest.fixture(scope="session")
def users_test_data() -> dict:
    return _read_json_test_data("users.json")


@pytest.fixture(scope="session")
def invalid_login_cases() -> list[dict]:
    return _read_csv_test_data("invalid_login_cases.csv")


@pytest.fixture(scope="function")
def login_page(driver) -> LoginPage:
    return _wait_for_login_screen(driver, timeout=30, attempts=2)


@pytest.fixture(scope="function", autouse=True)
def ensure_clean_start_state(driver):
    # Enforce a known baseline for every test, even if the test does not use page fixtures.
    _wait_for_login_screen(driver, timeout=30, attempts=2)


@pytest.fixture(scope="function")
def seed_standard_user_session(login_page, users_test_data):
    products = ProductsPage(login_page.driver)
    user = users_test_data["standard_user"]
    login_page.login(user["username"], user["password"])
    products.wait_until_loaded()
    yield login_page, products


@pytest.fixture(scope="function")
def seed_cart_with_item(seed_standard_user_session):
    login, products = seed_standard_user_session
    products.add_first_item_to_cart()
    yield login, products


def _capture_failure_artifacts(driver, nodeid: str):
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    test_name = nodeid.replace("/", "_").replace("::", "_")

    out_dir = os.path.join("reports", "artifacts")
    os.makedirs(out_dir, exist_ok=True)

    try:
        driver.get_screenshot_as_file(
            os.path.join(out_dir, f"{test_name}_{ts}.png")
        )
    except Exception:
        pass

    try:
        with open(
            os.path.join(out_dir, f"{test_name}_{ts}.xml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(driver.page_source)
    except Exception:
        pass


def pytest_generate_tests(metafunc):
    if "invalid_login_case" in metafunc.fixturenames:
        cases = _read_csv_test_data("invalid_login_cases.csv")
        ids = [case.get("case_id", f"case_{idx}") for idx, case in enumerate(cases)]
        metafunc.parametrize("invalid_login_case", cases, ids=ids)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def driver(request):
    d = create_android_driver()
    try:
        yield d
    finally:
        rep = getattr(request.node, "rep_call", None)
        if rep and rep.failed:
            _capture_failure_artifacts(d, request.node.nodeid)

        try:
            d.quit()
        except Exception:
            pass
