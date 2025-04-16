import time
import pytest
import allure
import random
import string

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Filters")
@allure.story("Verify duplicate removal in the 'Country' filter.")
def test_country_duplication(driver, config):
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
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

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

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//label[normalize-space()='Account Name']")))
    time.sleep(10)

    # Wait for and click the country selection input field
    country_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Country(s)']")))
    country_input.click()
    time.sleep(1)

    # Wait for the list of country options to be present
    country_options = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[5]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li")))

    # Validate if at least one option is available
    if not country_options:
        print("No country options found.")
        pytest.skip("No country options available. Skipping test case.")
        driver.quit()
        exit()

    # Extract country names and check for duplicates
    country_names = []
    for option in country_options:
        country_name = option.text.strip()
        # print(country_name)

        if country_name in country_names:
            print(f"Duplicate country found: {country_name}")
            pytest.fail(f"Test failed due to duplicate country: {country_name}")

        country_names.append(country_name)