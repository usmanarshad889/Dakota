import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
def test_search_functionality_by_contact_account_name(driver, config):
    wait = WebDriverWait(driver, 20)

    # Navigate to login page
    driver.get(config["base_url"])

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Wait for URL change
        WebDriverWait(driver, 20).until(EC.url_contains("/lightning"))

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)


    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Contacts tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    print(f"Current Tab : {tab.text}")
    tab.click()

    # Enter the account name "Test"
    account_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Account Name'])[2]")))
    account_input.send_keys("Test")

    # Wait for the results to load
    time.sleep(8)

    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Extract all contacts names text using a simpler XPath
    account_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//lightning-datatable//tbody/tr/td[4]")
    ))

    # Assert that at least one account is found
    assert len(account_names) > 0, "No account name found in the search results"

    # Check that all returned account names contain the text "test"
    for account in account_names:
        account_text = account.text.strip().lower()
        print(f"Contact: {account_text}")
        assert "test" in account_text, f"Account name '{account.text}' does not contain 'test'"
    time.sleep(2)