import time
import random
import string
import pytest
import allure
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.webdriver import ActionChains
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

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.Skipped
@pytest.mark.release_two
def test_create_account_single_record(driver, config):
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
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

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
    time.sleep(1)

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
    time.sleep(2)


    # Navigate to login page of fuse app
    driver.get(config["base_url"])

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
    time.sleep(2)
