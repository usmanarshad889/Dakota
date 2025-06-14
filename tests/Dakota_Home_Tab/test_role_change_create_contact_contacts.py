import time
import pytest
import allure
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

@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Job Changes (Create Account from Account)")
@allure.story("Test creation of accounts directly from Job Changes - Account Name")
@pytest.mark.all
@pass_broken
def test_role_change_creation_of_account_from_account(driver, config):
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # Login block
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")

    # Confirm login success
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='App Launcher']")))
        print("App Launcher is found")
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to missing App Launcher: {type(e).__name__}")

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Role Changes']")))
    print(f"Section Name : {btn.text}")
    btn.click()

    # Wait for records display
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Last Updated Date'])[1]")))
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")

    # Locate all Account Names
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[2]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[4]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-custom-cell[1]/c-custom-link-field[1]/lightning-button[1]/button[1]'''
    elements = driver.find_elements(By.XPATH, xpath)

    print(f" Total elements present : {len(elements)}")

    if len(elements) == 0:
        pytest.skip("No Account or Contact found that requires creation or linking. Skipping test case.")

    # Click on first unlinked account
    for element in elements:
        try:
            # Skip elements with zero size
            size = element.size
            if size['width'] == 0 or size['height'] == 0:
                continue
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)
            contact_name = element.text.strip()
            element.click()

            # Check if the account has right permission or not
            try:
                toast = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
                toast_message = toast.text
                # Check if the message is "You do not have permission rights to access this record."
                if toast_message == "You do not have permission rights to access this record.":
                    print(f"Permission error for account: {contact_name}. Trying next element...")
                    time.sleep(5)
                    continue  # Skip to the next element in the loop
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error: {type(e).__name__}")

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__} while clicking {element.text}")
        break


    # Click on Create Account and Related Contact
    link_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Account & Related Contacts']")))
    link_btn.click()
    time.sleep(15)

    # Check if "Create Account" button exists
    create_account_buttons = driver.find_elements(By.XPATH, "//button[normalize-space()='Create Account']")

    if create_account_buttons:
        create_account = wait.until(EC.element_to_be_clickable(create_account_buttons[0]))
        create_account.click()

        # Wait for toast message
        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Toast message: {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        # Verify the Toast message
        assert "are inserted successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"

    else:
        # Add Account with Related Contact(s)
        check_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")))
        check_box.click()

        # click on save/create button
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save and Create']")))
        save_btn.click()

        # Wait for toast message
        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Toast message: {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        # Verify the Toast message
        assert "are inserted successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"

