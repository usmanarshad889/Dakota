import time
import random
import string
import pytest
import allure
import datetime
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
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
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Mapping - Account field Mapping")
@allure.story("Validate successful mapping of account fields.")
def test_sync_of_new_accounts_created_by_create_task(driver, config):
    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 20)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["uat_username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["uat_password"])
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


    # Navigate to login page of fuse app
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

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

    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")


    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[5]")))
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
                select.select_by_visible_text("Create Task")
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
                select.select_by_visible_text("Owner")
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

    # Define the stopping condition element
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        # Refresh page and clear cookies
        driver.refresh()

        # Wait for search input and enter the search term
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchTerm']")))
        name_input.clear()
        name_input.send_keys(name_var)

        search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))

        # Double-click search button multiple times until condition is met
        actions = ActionChains(driver)
        for _ in range(3):
            if driver.find_elements(*stopping_condition_locator):
                print("Stopping condition met. Exiting loop.")
                break

            actions.double_click(search_element).perform()

        # If element is found, exit the while loop
        if driver.find_elements(*stopping_condition_locator):
            break

        attempts += 1  # Increment attempt counter

    # Fail test if maximum attempts reached and condition is not met
    assert attempts < max_attempts, "Test failed: Stopping condition not met after 5 attempts"

    # Check for checkboxes after exiting loop
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)


    # Check for account linking icon
    # Define the stopping condition element
    stopping_condition_locator = (By.XPATH, "//th[@class='test']//lightning-icon[@class='slds-m-left_x-small slds-m-right_x-small slds-icon_container_circle slds-icon-action-share-link slds-icon_container']")

    max_attempts = 10
    attempts = 0

    while attempts < max_attempts:
        # Refresh page and clear cookies
        driver.refresh()

        # Wait for search input and enter the search term
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchTerm']")))
        name_input.clear()
        name_input.send_keys(name_var)

        search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))

        # Double-click search button multiple times until condition is met
        actions = ActionChains(driver)
        for _ in range(3):
            if driver.find_elements(*stopping_condition_locator):
                print("Stopping condition met. Exiting loop.")
                break

            actions.double_click(search_element).perform()

        # If element is found, exit the while loop
        if driver.find_elements(*stopping_condition_locator):
            break

        attempts += 1  # Increment attempt counter

    # Fail test if maximum attempts reached and condition is not met
    assert attempts < max_attempts, "Test failed: Stopping condition not met after 5 attempts"

    # Check for checkboxes after exiting loop
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(3)


    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/o/Task/home")

    # Select Table View
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Select list display']")))
        time.sleep(1)
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Table']//lightning-primitive-icon[@size='x-small']")))
        btn.click()
        print("Successfully click Table view")
    except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")
    time.sleep(5)


    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Select a List View: Tasks']//lightning-primitive-icon[@exportparts='icon']//*[name()='svg']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class=' virtualAutocompleteOptionText'][normalize-space()='Open Tasks']")))
        btn.click()
        print("Successfully Click on Opened Task")
    except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")
    time.sleep(5)


    src_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search this list...']")))
    src_button.send_keys("Dakota Marketplace | Account Record Created")
    time.sleep(1)
    load_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@name,'refreshButton')]")))
    load_button.click()
    time.sleep(5)


    # found = False  # Flag to track if name_var is found
    #
    # # First attempt: Check before clicking refresh
    # try:
    #     all_accounts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[4]")))
    #     account_texts = [account.text.strip() for account in all_accounts]
    #
    #     if name_var in account_texts:
    #         found = True  # Mark as found
    # except (NoSuchElementException, TimeoutException) as e:
    #     print(f"Message: {type(e).__name__}")
    #
    # # Click on the "Due Date" button
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@title,'Due Date')]")))
    # btn.click()
    #
    # # Wait and click on the refresh button
    # time.sleep(5)
    # load_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@name,'refreshButton')]")))
    # load_button.click()
    #
    # # Second attempt: Check after refresh
    # time.sleep(5)
    # try:
    #     all_accounts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td[4]")))
    #     account_texts = [account.text.strip() for account in all_accounts]
    #
    #     if name_var in account_texts:
    #         found = True  # Mark as found
    # except (NoSuchElementException, TimeoutException) as e:
    #     print(f"Message: {type(e).__name__}")
    #
    # # Final assertion
    # assert found, f"Account '{name_var}' not found in any attempt."
    # time.sleep(2)


    # Get today date
    today = datetime.datetime.today()
    today_date = f"{today.month}/{today.day}/{today.year}"
    print(today_date)

    found = False  # Flag to track if today's due date is found

    # First attempt: Check before clicking refresh
    try:
        all_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='uiOutputDate']")))
        date_texts = [date.text.strip() for date in all_dates if date.text.strip()]  # Filter out empty texts

        if today_date in date_texts:
            print("A Task with today's due date is found in the first attempt. Test Passed!")
            found = True  # Mark as found
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")

    # If not found in the first attempt, proceed with refresh
    if not found:
        # Click on the "Due Date" button
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@title,'Due Date')]"))).click()

        # Click on the refresh button
        time.sleep(5)  # Allow UI update time
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@name,'refreshButton')]"))).click()

        # Second attempt: Check after refresh
        time.sleep(5)  # Allow refreshed elements to load
        try:
            all_dates = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[@class='uiOutputDate']")))
            date_texts = [date.text.strip() for date in all_dates if date.text.strip()]

            if today_date in date_texts:
                print("A Task with today's due date is found after refresh. Test Passed!")
                found = True  # Mark as found
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")

    # Final assertion
    assert found, f"Test Failed: No Task is present with today's due date ({today_date})."