from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find(driver, locator):
    by, value = locator
    return driver.find_element(by, value)

def wait_for(driver, locator, timeout=15):
    by, value = locator
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def safe_click(driver, locator, timeout=15):
    """
    Tries click first. If element exists but isn't 'clickable' (common in Android ViewGroups),
    fall back to a W3C click gesture using elementId.
    """
    el = wait_for(driver, locator, timeout=timeout)
    try:
        el.click()
        return
    except Exception:
        # Appium gesture fallback
        driver.execute_script("mobile: clickGesture", {"elementId": el.id})
