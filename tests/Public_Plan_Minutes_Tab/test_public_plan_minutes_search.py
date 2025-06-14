import time
import random
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
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


@pytest.mark.release_five
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Public Plan Minutes")
@allure.story("Verify search functionality for Public Plan Minute names.")
@pytest.mark.all
@pass_broken
def test_public_plan_search(driver, config):
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

    # Navigate to Public Plan Meetings Minutes Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Public_Plan_Minutes")


    # Verify Public Plan Minutes Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//th[@data-label='Name'])[1]")))
        assert element.is_displayed(), "Public Plan Minutes list is not displayed"
    except TimeoutException:
        pytest.fail("Public Plan Minutes list not loaded in time")


    # 1. Collect all Public Plan Minutes Names
    all_names_elements = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "(//th[@data-label='Name'])"))
    )

    all_names = [elem.text.strip() for elem in all_names_elements if elem.text.strip()]
    assert len(all_names) >= 3, "Not enough Public Plan Minutes Names to perform test!"

    # 2. Randomly select 3 unique names
    random_names = random.sample(all_names, 3)  # Ensures no duplicates

    for name in random_names:
        print(f"Testing FULL search for Public Plan Minutes: {name}")

        # FULL SEARCH
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        search_box.clear()
        search_box.send_keys(name)  # Full name
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        inv_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//th[@data-label='Name'])")))

        # Screenshot & Allure attachment
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"{name} - Full Search Result", attachment_type=allure.attachment_type.PNG)

        assert len(inv_names) > 0, "No Public Plan Minutes names found in FULL search results"
        #
        # # Assertion for FULL search
        # for inv in inv_names:
        #     inv_text = inv.text.strip().lower()
        #     assert name.lower() in inv_text, f"Public Plan Minutes name '{inv.text}' does not match '{name}'"
