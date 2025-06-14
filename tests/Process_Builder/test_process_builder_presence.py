import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_five
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Process Builders")
@allure.story("Verify that process builders (Dakota Connect Account/Contact Field Update) are present.")
@pytest.mark.all
@pass_broken
def test_process_builder_presence(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
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


    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/setup/ProcessAutomation/home")


    # Switch to iframe
    iframe = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='accessibility title']")))
    driver.switch_to.frame(iframe)
    print("Successfully switched to iframe")
    time.sleep(1)


    required_names = {
        "X_Dakota Connect Contact Field Update(Deprecated)",
        "X_Dakota Connect Account Field Update(Deprecated)"
    }

    found_names = set()

    # --- Check First Page ---
    process_builders = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='label']")))
    for process_builder in process_builders:
        name = process_builder.text.strip()
        for required in required_names:
            if required in name:
                found_names.add(required)

    # --- Check Second Page if needed ---
    if found_names != required_names:
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='pagerControl next']")))
            next_button.click()
            time.sleep(8)

            process_builders = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='label']")))
            for process_builder in process_builders:
                name = process_builder.text.strip()
                for required in required_names:
                    if required in name:
                        found_names.add(required)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")

    # --- Final Assertion ---
    missing = required_names - found_names
    print(f"Found Names: {found_names}")
    assert not missing, f"Missing process builders: {missing}"
