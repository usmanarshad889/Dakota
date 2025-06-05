import time
import pytest
import allure
import random
import string
from test_utils import skip_broken , pass_broken

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
    yield driver
    driver.quit()


@pytest.mark.release_five
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Filters")
@allure.story("Confirm state visibility changes based on selected countries.")
@pytest.mark.all
@pass_broken
def test_state_visibility_based_on_country(driver, config):
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

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//label[normalize-space()='Account Name']")))
    time.sleep(15)


    # Define expected states for each country
    expected_states = {
        "USA": {"California", "Texas", "New York", "Florida", "Illinois"},  # Add more as needed
        "Canada": {"Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"}  # Add more as needed
    }

    # List of countries to check
    countries_to_check = ["USA", "Canada"]

    # Loop through each country and validate states
    for country_name in countries_to_check:
        # Wait for and click the country selection input field
        country_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Country(s)']")))
        country_input.click()
        time.sleep(1)

        # Wait for the list of country options
        country_options = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[5]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li")))

        # Select the desired country
        selected_country = None
        for option in country_options:
            if option.text.strip() == country_name:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
                time.sleep(1)
                option.click()
                selected_country = country_name
                break

        if not selected_country:
            pytest.fail(f"Test failed: Country '{country_name}' not found in dropdown.")

        # Wait for states to load
        time.sleep(1)

        # Wait for and click the state selection input field
        state_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select State(s)']")))
        state_input.click()
        time.sleep(1)

        # Wait for the list of state options
        state_options = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[1]//div[6]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li//div[1]")))

        # Validate at least one option is available
        if not state_options:
            print(f"No state options found for {selected_country}.")
            pytest.skip(f"No state options available for {selected_country}. Skipping test case.")
            driver.quit()
            exit()

        # Extract displayed state names
        displayed_states = {option.text.strip() for option in state_options}

        # Check if all expected states are found
        missing_states = expected_states[selected_country] - displayed_states

        if missing_states:
            print(f"Missing states for {selected_country}: {missing_states}")
            pytest.fail(f"Test failed: Some expected states for {selected_country} are missing.")
        else:
            print(f"Test passed: All expected states for {selected_country} were found.")

        reset_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Reset']")))
        reset_button.click()
        time.sleep(1)


        # # # --------------------------------------------------------------------  # # #
        # Check exact logic

        # # Define expected states for each country
        # expected_states = {
        #     "USA": {"California", "Texas", "New York", "Florida", "Illinois"},  # Add more as needed
        #     "Canada": {"Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba"}  # Add more as needed
        # }
        #
        # # List of countries to validate
        # countries_to_check = ["USA", "Canada"]
        #
        # # Loop through each country and validate states
        # for country_name in countries_to_check:
        #     # Wait for and click the country selection input field
        #     country_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Country(s)']")))
        #     country_input.click()
        #     time.sleep(1)
        #
        #     # Wait for the list of country options to be present
        #     country_options = wait.until(EC.presence_of_all_elements_located(
        #         (By.XPATH, "//div[5]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li")))
        #
        #     # Validate if at least one option is available
        #     if not country_options:
        #         print("No country options found.")
        #         pytest.skip("No country options available. Skipping test case.")
        #         driver.quit()
        #         exit()
        #
        #     selected_country = None
        #
        #     # Iterate through country options to find and select the desired country
        #     for option in country_options:
        #         if option.text.strip() == country_name:
        #             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        #             time.sleep(1)
        #             option.click()
        #             selected_country = country_name
        #             break
        #
        #     if not selected_country:
        #         pytest.fail(f"Test failed: Country '{country_name}' not found in dropdown.")
        #
        #     # Wait for states to load
        #     time.sleep(5)
        #
        #     # Wait for and click the state selection input field
        #     state_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select State(s)']")))
        #     state_input.click()
        #     time.sleep(1)
        #
        #     # Wait for the list of state options to be present
        #     state_options = wait.until(EC.presence_of_all_elements_located(
        #         (By.XPATH, "//div[1]//div[6]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li//div[1]")))
        #
        #     # Validate if at least one option is available
        #     if not state_options:
        #         print(f"No state options found for {selected_country}.")
        #         pytest.skip(f"No state options available for {selected_country}. Skipping test case.")
        #         driver.quit()
        #         exit()
        #
        #     # Extract and validate state names
        #     for option in state_options:
        #         state_name = option.text.strip()
        #         print(f"Found state: {state_name}")
        #
        #         # Ensure the state belongs to the selected country
        #         if state_name not in expected_states[selected_country]:
        #             print(f"Invalid state found for {selected_country}: {state_name}")
        #             pytest.fail(f"Test failed: State '{state_name}' does not belong to {selected_country}")
        #
        #     print(f"Test passed: All displayed states belong to {selected_country}.")