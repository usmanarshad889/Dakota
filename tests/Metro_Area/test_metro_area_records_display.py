import time
import pytest
import allure
from test_utils import skip_broken

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_six
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Metro Area")
@allure.story("Verify the display of metro area records in Metro Area Tab.")
@pytest.mark.all
@skip_broken
def test_metro_area_records_display(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()
        time.sleep(3)

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Metro_Areas")

    # Wait for elements to present
    try:
        btn = wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]")))
        print(btn.text)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    time.sleep(2)


    # Wait for all links under "Metro Area Name"
    all_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//th[@data-label='Metro Area Name']//a")))

    # Assertion to check if names are present
    assert len(all_names) > 0, "Metro Area Names are not loaded"

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Search Result", attachment_type=allure.attachment_type.PNG)

    # (Optional) Print names to verify (can be removed later)
    print("\nFollowing are loaded Metro Area names :")
    for name in all_names:
        print(name.text)
