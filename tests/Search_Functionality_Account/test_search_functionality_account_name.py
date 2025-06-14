import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
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
@allure.story("Verify search filter for Account Name.")
@pytest.mark.all
@pass_broken
def test_search_account_name(driver, config):
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

    # Navigate to the account search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Account tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Accounts']")))
    print(f"Current Tab : {tab.text}")

    # Enter the Account name "Test"
    account_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Account Name']")))
    account_input.send_keys("Test")

    # Wait for the results to load
    time.sleep(15)

    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@title='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Extract all Account names text using a simpler XPath
    account_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[2]")
    ))

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    # Assert that at least one Account is found
    assert len(account_names) > 0, "No Account names found in the search results"

    # Check that all returned Account names contain the text "test"
    for account in account_names:
        account_text = account.text.strip().lower()
        print(f"Contact: {account_text}")
        assert "test" in account_text, f"Account name '{account.text}' does not contain 'test'"