import os
import pytest
from datetime import datetime, timezone
from src.core.driver_factory import create_android_driver


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def driver(request):
    d = create_android_driver()
    yield d

    # Only capture artifacts if the test failed
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        test_name = request.node.nodeid.replace("/", "_").replace("::", "_")

        out_dir = os.path.join("reports", "artifacts")
        os.makedirs(out_dir, exist_ok=True)

        # Screenshot
        d.get_screenshot_as_file(
            os.path.join(out_dir, f"{test_name}_{ts}.png")
        )

        # Page source
        with open(
            os.path.join(out_dir, f"{test_name}_{ts}.xml"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(d.page_source)

    d.quit()
