import time
import random
import pytest
import allure
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Faker
fake = Faker()
phone = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
mobile = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
mailing_address = fake.address()
account_name = fake.company()
name = fake.name()
first_name = fake.first_name()
last_name = fake.last_name()
suffix = random.choice(['Jr.', 'Sr.', 'III', 'PhD', 'MD', 'Esq.'])
email = fake.email()
title = fake.job()
contact_type = random.choice(['Personal', 'Business', 'Emergency', 'Billing'])
search_name = "Test" + " " + last_name

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_icon_display_unlinking(driver, config):
    driver.get("https://test.salesforce.com/")
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys("draftsf@draftdata.com.uat")
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys("Rolustech@99")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Move to account Tab and click on new button
    driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/lightning/o/Contact/list")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    new_button.click()
    time.sleep(2)

    # Select a record type
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
    new_button.click()

    # Select account name
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    name_field.send_keys(phone)

    # Select phone
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']")))
    field.send_keys(mobile)

    element = driver.find_element(By.XPATH, "//input[@name='city']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='LinkedIn_URL__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = driver.find_element(By.XPATH, "//input[@name='GHIN__c']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    # SELECT Account type
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search Accounts...']")))
    input_field.clear()
    input_field.send_keys("Test Contacts")
    dropdown_option = wait.until(EC.visibility_of_element_located((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[2]")))
    dropdown_option.click()
    time.sleep(2)

    # Select account name
    salutation_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='salutation']")))
    salutation_field.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//lightning-base-combobox-item[@data-value='Mr.']").click()

    # Select First name
    driver.find_element(By.XPATH, "//input[@name='firstName']").send_keys("Test")
    # driver.find_element(By.XPATH, "//input[@name='middleName']").send_keys(middle_name)
    driver.find_element(By.XPATH, "//input[@name='lastName']").send_keys(last_name)
    driver.find_element(By.XPATH, "//input[@name='suffix']").send_keys(suffix)
    driver.find_element(By.XPATH, "//input[@name='Marketplace_Verified_Contact__c']").click()
    time.sleep(1)

    element = driver.find_element(By.XPATH, "//input[@name='suffix']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@name='Email']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@name='Title']").send_keys(title)
    driver.find_element(By.XPATH, "//button[@aria-label='Contact Type']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//lightning-base-combobox-item[@data-value='Administrator']").click()

    # click on save button
    driver.find_element(By.XPATH, "//button[@name='SaveEdit']").click()
    time.sleep(15)

    # Navigate to login page of fuse app
    driver.get(config["base_url"])

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

    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()
    time.sleep(5)
    driver.refresh()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()
    time.sleep(15)

    try:
        # Search by name
        driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").clear()
        driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").send_keys(search_name)
        driver.find_element(By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
        time.sleep(10)
    except:
        print("Filter not working")

    driver.refresh()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()
    time.sleep(15)

    try:
        # Search by name
        driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").clear()
        driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").send_keys(search_name)
        driver.find_element(By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
        time.sleep(10)
    except:
        print("Filter not working")

    driver.find_element(By.XPATH, "(//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small'])[1]").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//span[normalize-space()='Link Contact']").click()
    time.sleep(10)

    # Link account
    all_buttons = driver.find_elements(By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")
    for button in all_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", button)
        if button.is_enabled():
            button.click()
            time.sleep(1)
            break

    time.sleep(12)

    try:
        driver.find_element(By.XPATH, "//lightning-primitive-icon[@size='small']//*[name()='svg']").click()
        time.sleep(10)
    except:
        pass

    # Search by name
    driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").clear()
    driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").send_keys(search_name)

    driver.find_element(By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
    time.sleep(10)

    # Unlink that account
    driver.find_element(By.XPATH, "(//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small'])[1]").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//span[normalize-space()='Unlink Contact']").click()
    time.sleep(10)

    driver.find_element(By.XPATH, "//button[normalize-space()='Unlink']").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[normalize-space()='Yes']").click()
    time.sleep(10)

    # Search by name
    driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").clear()
    driver.find_element(By.XPATH, "(//input[@name='searchTerm'])[2]").send_keys(search_name)

    driver.find_element(By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
    time.sleep(10)

    # Test the icon
    svg_icon = driver.find_elements(By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")
    if svg_icon:
        assert False
    else:
        assert True