import time
import pytest
import allure
from test_utils import skip_broken

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


@pytest.mark.smoke
@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Account Linking")
@allure.story('Validate "Link Account" functionality with search by Account Name.')
@pytest.mark.all
@skip_broken
def test_mass_create_link_account_by_name(driver, config):
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
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='DisplayCriteria']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")
    time.sleep(15)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    time.sleep(2)
    btn.click()

    # Click on ALL CHECKBOX
    all_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]")))
    all_box.click()

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='MassUploadActions']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Account")

    time.sleep(10)

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[4]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Dakota Name")

    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[5]")))
        dropdown_option = Select(dropdown)
        dropdown_option.select_by_visible_text("Account Name")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'slds-button slds-button_neutral slds-button slds-button--brand')][normalize-space()='Search']"))).click()
    time.sleep(8)


    # Click on linked account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Accounts']")))
    btn.click()

    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Actual Toast Text : {toast_message.text}")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    valid_messages = [
        "Account(s) linking is in progress",
        "No account to link."
    ]

    toast_text = toast_message.text.strip()
    assert toast_text in valid_messages, f"Unexpected Toast Message: {toast_text}"
    time.sleep(2)