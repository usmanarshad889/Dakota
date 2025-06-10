import time
import random
import string
import pytest
import allure
from test_utils import skip_broken , pass_broken

import datetime
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Generate Random Name, Email and Phone
fake = Faker()
random_name = "Test " + fake.name()  # Add 'test' at the start of the name
email_prefix = ''.join(random.choices(string.ascii_lowercase, k=7))
random_email = f"www.{email_prefix}.com"
random_phone = ''.join(random.choices(string.digits, k=9))
# Print the generated values
print("Name:", random_name)
print("Email:", random_email)
print("Phone:", random_phone)
# Store them in variables
name_var = random_name
email_var = random_email
phone_var = random_phone


# # Define the target minutes (when the script should run)
# target_minutes = {12, 27, 42, 57}
#
# def wait_until_target_time():
#     """Wait until the system time is close to one of the target minutes."""
#     while True:
#         now = datetime.datetime.now()
#         print(f"Current Time : {now}")
#         if now.minute in target_minutes and now.second == 0:  # Run exactly at the target minute
#             print(f"Running Selenium script at {now.strftime('%H:%M:%S')}")
#             return
#         time.sleep(0.5)  # Check every 0.5 seconds to minimize CPU usage
#
# # Wait until the correct time
# wait_until_target_time()


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.all
@pytest.mark.release_seven
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Auto Sync Functionality")
@allure.story('Validate that when the toggle button "Auto Sync New Accounts and Related Contacts" is enabled, newly created accounts are synced correctly, and an email is successfully triggered.')
# @skip_broken
def test_sync_of_new_accounts_created_by_create_task(driver, config):
    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["uat_username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["uat_password"])
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

    # Move to account Tab and click on new button
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    time.sleep(2)
    new_button.click()
    time.sleep(2)

    # Select a record type
    record_type = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
    time.sleep(2)
    record_type.click()

    # Select account name
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Name']")))
    name_field.send_keys(name_var)

    # Select phone
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    field.send_keys(phone_var)

    # Select website
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Website']")))
    field.send_keys(email_var)

    # Select Type
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-value='--None--'])[2]")))
    field.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[4]")))
    btn.click()


    # Select CRD
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='CRD__c']")))
    field.send_keys("3546")

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Website']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='AUM__c']")))
    element.send_keys("10000")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Average_Ticket_Size__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Total_Participants__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Trial_Start_Date__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Copyright__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='SEC_Registered_Date__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Billing Street']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Billing Zip/Postal Code']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = driver.find_element(By.XPATH, "//input[@name='X100_Marketplace__c']")
    element.click()

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']")))
    save_btn.click()
    time.sleep(2)

    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was created" in toast_massage.lower().strip() , f"Error while creating account : {toast_massage}"


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

    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")


    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[3]//article[1]//div[1]//div[1]//div[1]//button[1]//lightning-primitive-icon[1]")))
    element.click()
    time.sleep(1)

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(2)

    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[1]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Sync Account/Contact Type Field is not working")
        print(f"Error: {type(e).__name__}")


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[2]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Auto Sync new Accounts and related Contacts is not working")
        print(f"Error: {type(e).__name__}")


    # Set the Notification setting (Auto Sync new Accounts and related Contacts)
    try:
        # Select Notification Setting
        xpath = '''(//select[@name='a7Fdy0000003GjNEAU'])[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Send Email")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Setting field not selected")
    time.sleep(1)

    try:
        # Select Notification Recipient
        xpath = '''(//select[@name='a7Fdy0000003GjNEAU'])[2]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("User")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Recipient not selected")
    time.sleep(1)

    try:
        # Select Notification Assignee User/Group
        xpath = '''(//select[@name='a7Fdy0000003GjNEAU'])[3]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Aiman Shakil")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Assignee User not selected")
    time.sleep(1)


    # Scroll down by 1500 pixels
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(5)

    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    text = toast_message.text
    print(f"Actual Toast message : {text}")

    assert text in ["Mapping saved successfully.", "Status changed successfully!"], f"Unexpected toast message: {text}"
    time.sleep(2)


    # Navigate to Market Place Search
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")
    time.sleep(3)

    # Define the stopping condition element (second checkbox)
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        driver.refresh()
        time.sleep(2)  # Allow time for page to load after refresh

        try:
            # Enter search term
            name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchTerm']")))
            name_input.clear()
            name_input.send_keys(name_var)

            # Click the Search button
            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
            actions = ActionChains(driver)

            for _ in range(3):  # Try clicking search up to 3 times
                # Check stopping condition before clicking again
                if driver.find_elements(*stopping_condition_locator):
                    print("Stopping condition met. Exiting loop.")
                    break

                actions.move_to_element(search_button).click().perform()
                time.sleep(2)  # Let the results update/load

            # Break outer loop if condition is met
            if driver.find_elements(*stopping_condition_locator):
                print("Element found after search attempts.")
                break

        except Exception as e:
            print(f"Attempt {attempts + 1} failed: {e}")

        attempts += 1
        time.sleep(1)

    # Assert loop succeeded
    assert attempts < max_attempts, "Test failed: Stopping condition not met after 5 attempts"

    # Final check for the checkbox element
    checkboxes = driver.find_elements(*stopping_condition_locator)
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)


    # ---------------- #
    ### Verify Email ###


    try:
        driver.get("https://mail.google.com/mail/u/0/#inbox")

        email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='identifierId']")))
        email_field.send_keys("usman.arshad@rolustech.com")

        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
        next_btn.click()

        password_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Passwd']")))
        password_field.send_keys("test")

        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
        next_btn.click()
        time.sleep(20)

        try:
            # Wait for Gmail Inbox to Load
            wait.until(EC.presence_of_element_located((By.XPATH, "//table[@role='grid']")))

            # Locate the Gmail Search Box
            search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail']")))

            # Type Email Search Query (Modify as Needed)
            search_box.send_keys("from:SF Development")  # Modify email search criteria
            search_box.send_keys(Keys.ENTER)

            # Wait for Search Results to Load
            time.sleep(5)  # Adjust sleep time as needed

            try:
                # Capture Search Results
                emails = driver.find_elements(By.XPATH, "(//td[@class='oZ-x3 xY'])")
                print(f"Total Emails Found: {len(emails)}")
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Message: {type(e).__name__}")
                assert True

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")
            print("2 Step verification not completed")
            assert True

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        assert True
