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
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["uat_username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["uat_password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(2)

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
    time.sleep(2)

    xpath = '''//li//lst-related-list-quick-link//div//div//records-hoverable-link//div'''
    all_links = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    for link in all_links:
        if "Related Contacts" in link.text:
            link.click()
            time.sleep(10)
            break