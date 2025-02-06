import time
import random
import openpyxl
import os
import string
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Generate Random Name, Email and Phone
fake = Faker()
random_name = "Test " + fake.name()  # Add 'test' at the start of the name
email_prefix = ''.join(random.choices(string.ascii_lowercase, k=7))
random_email = f"https://www.{email_prefix}.com"
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

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_display_icon_linking(driver, config):
    driver.get("https://test.salesforce.com/")
    wait = WebDriverWait(driver, 10)
    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys("draftsf@draftdata.com.uat")
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys("Rolustech@99")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Move to account Tab and click on new button
    driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/lightning/o/Account/list?filterName=__Recent")
    new_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    new_button.click()
    time.sleep(2)

    # Select a record type
    new_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
    new_button.click()

    # Select account name
    name_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Name']")))
    name_field.send_keys(name_var)

    # Select phone
    field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    field.send_keys(phone_var)

    # Select website
    field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Website']")))
    field.send_keys(email_var)

    element = driver.find_element(By.XPATH, "//input[@name='Website']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = driver.find_element(By.XPATH, "//input[@name='AUM__c']")
    element.send_keys("10000")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = driver.find_element(By.XPATH, "//input[@name='Average_Ticket_Size__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='Total_Participants__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='Trial_Start_Date__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='Copyright__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='SEC_Registered_Date__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='X100_Marketplace__c']")
    element.click()
    time.sleep(1)

    # click on save button
    driver.find_element(By.XPATH, "//button[@name='SaveEdit']").click()
    time.sleep(10)

    # Define the Excel file path
    file_path = "test_data.xlsx"

    # Check if the file exists
    if os.path.exists(file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["Name", "Email", "Phone"])  # Add header row if file is new

    # Append the generated data to the Excel file
    sheet.append([name_var, email_var, phone_var])

    # Save the file
    workbook.save(file_path)

    # Navigate to login page of fuse app
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])

    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Navigate to Market Place Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(5)

    driver.refresh()
    time.sleep(15)

    # Search by name
    driver.find_element(By.XPATH, "//input[@name='searchTerm']").send_keys(name_var)
    driver.find_element(By.XPATH, "//button[@title='Search']").click()
    time.sleep(10)

    driver.refresh()
    time.sleep(15)

    # Search by name
    driver.find_element(By.XPATH, "//input[@name='searchTerm']").send_keys(name_var)
    driver.find_element(By.XPATH, "//button[@title='Search']").click()
    time.sleep(10)

    # Test the icon
    svg_icon = driver.find_elements(By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")
    if svg_icon:
        assert False
    else:
        assert True

    driver.find_element(By.XPATH, "(//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small'])[1]").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//span[normalize-space()='Link Account']").click()
    time.sleep(10)

    # Search account
    driver.find_element(By.XPATH, "//input[@placeholder='Search Accounts']").send_keys("Test")
    driver.find_element(By.XPATH, "//div[contains(@class,'resetButtonDiv')]//button[contains(@type,'button')][normalize-space()='Search']").click()
    time.sleep(5)

    # Link account
    all_buttons = driver.find_elements(By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")
    for button in all_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", button)
        if button.is_enabled():
            button.click()
            time.sleep(1)
            break

    time.sleep(10)

    try:
        driver.find_element(By.XPATH, "//lightning-primitive-icon[@size='small']//*[name()='svg']").click()
        time.sleep(5)
    except:
        pass

    # Search by name
    driver.find_element(By.XPATH, "//input[@name='searchTerm']").clear()
    driver.find_element(By.XPATH, "//input[@name='searchTerm']").send_keys(name_var)

    driver.find_element(By.XPATH, "//button[@title='Search']").click()
    time.sleep(10)

    # Test the icon
    svg_icon = driver.find_elements(By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")
    if svg_icon:
        assert True
    else:
        assert False