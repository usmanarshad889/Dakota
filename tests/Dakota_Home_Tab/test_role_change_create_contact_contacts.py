import time
import pytest
import allure
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
@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Job Changes (Create Account from Account)")
@allure.story("Test creation of accounts directly from Job Changes - Account Name")
def test_role_change_creation_of_account_from_account(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
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
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Role Changes']")))
    print(f"Section Name : {btn.text}")
    btn.click()

    # Locate all Account Names
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[2]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[4]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-custom-cell[1]/c-custom-link-field[1]/lightning-button[1]/button[1]'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    if not elements:
        pytest.skip("No elements found. Skipping test case.")

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
                toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
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

        # Verify the Toast message
        assert "are inserted successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"

        # Attach a screenshot of the final state
        allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)

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

        # Verify the Toast message
        assert "are inserted successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"

        # Attach a screenshot of the final state
        allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)
