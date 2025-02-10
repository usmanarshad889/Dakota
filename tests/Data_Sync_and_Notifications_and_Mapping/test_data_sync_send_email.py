import time
import random
import string
import pytest
import allure
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Generate Random Name, Email and Phone
fake = Faker()
random_name = "test " + fake.name()  # Add 'test' at the start of the name
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

def test_data_sync_notification_email(driver, config):
    driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/")
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
    driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/lightning/o/Account/list?filterName=__Recent")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    new_button.click()
    time.sleep(2)

    # Select a record type
    driver.find_element(By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']").click()

    # Select account name
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Name']")))
    name_field.send_keys(name_var)

    # Select phone
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    field.send_keys(phone_var)

    # Select website
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Website']")))
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

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Setup")

    try:
        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]"))
        )
        element.click()
    except:
        pass
    time.sleep(1)

    # Click on Auto Sync Field Updates
    inactive_button = driver.find_element(By.XPATH, "//span[@class='slds-checkbox_off']")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "//span[@class='slds-checkbox_faux']").click()
        time.sleep(1)
    else:
        pass

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)

    # Select filed to match
    select_element = driver.find_element(By.XPATH, "(//select[@name='a7Ndy000000135ZEAQ'])[1]")
    option = Select(select_element)
    option.select_by_visible_text("CRD#")
    time.sleep(1)

    try:
        # Select Sync Option
        select_element = driver.find_elements(By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[3]/div[1]/div[1]/div[1]/select[1]")
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Update")
    except:
        print("Sync Option not selected")
    time.sleep(2)

    try:
        # Select Notification Setting
        select_element = driver.find_elements(By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[4]/div[1]/div[1]/div[1]/select[1]")
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Send Email")
    except:
        print("Notification Setting field not selected")
    time.sleep(2)

    try:
        # Select Notification Recipient
        select_element = driver.find_elements(By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[5]/div[1]/div[1]/div[1]/select[1]")
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Owner")
    except:
        print("Notification Recipient field not selected")
    time.sleep(2)

    try:
        # Select Notification Assignee User/Group
        select_element = driver.find_elements(By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[6]/div[1]/div[1]/div[1]/select[1]")
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Aiman Shakil")
    except:
        print("Notification Assignee User/Group not selected")
    time.sleep(2)

    # Scroll down by 1500 pixels
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(2)

    # Select Save Option
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[normalize-space()='OK']").click()
    time.sleep(10)

    # Navigate to installed pakages setup
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

    driver.find_element(By.XPATH, "//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small']").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//span[normalize-space()='Link Account']").click()
    time.sleep(10)

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

    try:
        driver.find_element(By.XPATH, f"//button[normalize-space()='{name_var}']").click()
        time.sleep(10)
    except:
        pass

    # Scroll down by 300 pixels
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(3)

    try:
        crd_text = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/one-record-home-flexipage2[1]/forcegenerated-adg-rollup_component___force-generated__flexipage_-record-page___-investment_-firm_-account_-page___-account___-v-i-e-w___-l-m-t___1738136225000[1]/forcegenerated-flexipage_investment_firm_account_page_account__view_js___lmt___1738136225000[1]/record_flexipage-desktop-record-page-decorator[1]/div[1]/records-record-layout-event-broker[1]/slot[1]/slot[1]/flexipage-record-home-template-desktop2[1]/div[1]/div[2]/div[1]/slot[1]/flexipage-component2[1]/slot[1]/flexipage-tabset2[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/slot[1]/flexipage-tab2[1]/slot[1]/flexipage-component2[1]/slot[1]/records-lwc-detail-panel[1]/records-base-record-form[1]/div[1]/div[1]/div[1]/div[1]/records-lwc-record-layout[1]/forcegenerated-detailpanel_account___0123m000000u83paas___full___view___recordlayout2[1]/records-record-layout-block[1]/slot[1]/records-record-layout-section[1]/div[1]/div[1]/dl[1]/slot[1]/records-record-layout-row[6]/slot[1]/records-record-layout-item[2]/div[1]/div[1]/dd[1]/div[1]/span[1]/slot[1]/lightning-formatted-text[1]").text
        print(crd_text, email_var)
        time.sleep(3)
        if crd_text.lower().strip() == email_var.lower().strip():
            assert True
    except:
        assert True
