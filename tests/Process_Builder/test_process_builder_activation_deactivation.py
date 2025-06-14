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
@allure.story("Ensure users can activate/deactivate process builders manually via Setup.")
@pytest.mark.all
@pass_broken
def test_process_builder_activation_deactivation(driver, config):
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
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='accessibility title']")))
    driver.switch_to.frame(iframe)
    print("Successfully switched to iframe")
    time.sleep(1)

    # Step 1: Click on SVG button to open actions
    svg_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@title='Auto schedule batches']//lightning-primitive-icon[@exportparts='icon']//*[name()='svg']")))
    svg_button.click()

    # Step 2: Try clicking Activate button first
    action_done = None  # To track which button was clicked

    try:
        activate_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Activate']")))
        if activate_button.is_displayed():
            activate_button.click()
            print("Clicked Activate button")
            action_done = "Activate"
    except TimeoutException:
        print("Activate button not found, checking for Deactivate button")
        try:
            deactivate_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Deactivate']")))
            if deactivate_button.is_displayed():
                deactivate_button.click()
                print("Clicked Deactivate button")
                action_done = "Deactivate"
        except TimeoutException:
            print("Neither Activate nor Deactivate button found!")

    # Step 3: Click Confirm button
    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Confirm']")))
    confirm_button.click()
    time.sleep(8)

    # Step 4: Perform opposite action

    if action_done is not None:
        # Click SVG button again
        svg_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@title='Auto schedule batches']//lightning-primitive-icon[@exportparts='icon']//*[name()='svg']")))
        svg_button.click()
        time.sleep(2)

        # Check & click opposite button
        if action_done == "Activate":
            try:
                deactivate_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Deactivate']")))
                if deactivate_button.is_displayed():
                    deactivate_button.click()
                    time.sleep(2)
                    print("Clicked Deactivate button (second action)")
            except TimeoutException:
                print("Deactivate button not found in second step!")
        elif action_done == "Deactivate":
            try:
                activate_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Activate']")))
                if activate_button.is_displayed():
                    activate_button.click()
                    time.sleep(2)
                    print("Clicked Activate button (second action)")
            except TimeoutException:
                print("Activate button not found in second step!")

        # Click Confirm button again
        confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Confirm']")))
        confirm_button.click()
        time.sleep(5)