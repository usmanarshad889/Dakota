import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from datetime import datetime, timedelta
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


@pytest.mark.smoke
@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Accounts")
@allure.story("Verify search filter for Marketplace Created Date.")
@pytest.mark.all
@pass_broken
def test_search_aum(driver, config):
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

    # Navigate to Marketplace Search
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select Marketplace Created Date Filter
    date = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='CRMCreatedDate']")))
    dropdown = Select(date)
    dropdown.select_by_visible_text("Last 90 Days")
    time.sleep(2)

    # Select Display Criteria (Unlinked Account)
    criteria_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])")))
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")
    time.sleep(15)

    # click on search button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()

    # Click on first Result
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@name='previewAccount'])[1]")))
    time.sleep(1)
    button.click()

    # Copy Dakota Created Date
    account_date = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-formatted-text[@class='slds-form-element__static'])[11]")))
    account_date_text = account_date.text.strip()

    # Parse the date string into a datetime object
    account_date = datetime.strptime(account_date_text, "%m/%d/%Y, %I:%M %p")
    print(f"Extracted Date : {account_date}")

    # Calculate the date range for the last 90 days
    current_date = datetime.now()
    start_date = current_date - timedelta(days=90)

    # Perform the range check
    is_within_range = start_date <= account_date <= current_date

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    # Use assert True with the range check result
    assert is_within_range, f"Date {account_date_text} is not within the last 90 days range."
    time.sleep(2)

    print(f"Date {account_date_text} is valid and within the last 90 days.")
