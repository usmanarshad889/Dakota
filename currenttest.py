import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define Selected Options in dropdown for Marketplace Account Fields (Account Name)
salesforce_account_fields = "Account Name"
sync_option = "Update"
notification_setting = "Create Task"
notification_recipient = "Group"
notification_assignee = "HRG"

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

# Open the Salesforce URL
driver.get("https://dakotanetworks--sand2024.sandbox.lightning.force.com/lightning/n/Marketplace__Investments")

# Log in
wait = WebDriverWait(driver, 10)
username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
username.clear()
username.send_keys("draftsf@draftdata.com.sand2024")

password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
password.clear()
password.send_keys("LOWYqfakgQ8oo")

login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
login_button.click()

# Wait for page to load
time.sleep(5)


# Navigate to installed pakages setup
driver.get("https://dakotanetworks--sand2024.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Setup")
time.sleep(15)

try:
    # Using class name (if applicable)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]"))
    )
    element.click()
    print("Clicked using CLASS_NAME")
except:
    pass
time.sleep(1)

# Click on Auto Sync Field Updates
driver.find_element(By.XPATH, "//span[@class='slds-checkbox_faux']").click()
time.sleep(1)

# Scroll down by 500 pixels
driver.execute_script("window.scrollBy(0, 500);")
time.sleep(10)

try:
    # Select Salesforce Account Fields
    select_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[1]/td[2]/div[1]/div[1]/div[1]/select[1]")
    select = Select(select_element)
    select.select_by_visible_text(salesforce_account_fields)
    time.sleep(1)
except:
    print("Salesforce Account Fields not selected")

try:
    # Select Sync Option
    select_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[1]/td[3]/div[1]/div[1]/div[1]/select[1]")
    select = Select(select_element)
    select.select_by_visible_text(sync_option)
    time.sleep(1)
except:
    print("Sync Option not selected")

try:
    # Select Notification Setting
    select_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[1]/td[4]/div[1]/div[1]/div[1]/select[1]")
    select = Select(select_element)
    select.select_by_visible_text(notification_setting)
    time.sleep(1)
except:
    print("Notification Setting field not selected")

try:
    # Select Notification Recipient
    select_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[1]/td[5]/div[1]/div[1]/div[1]/select[1]")
    select = Select(select_element)
    select.select_by_visible_text(notification_recipient)
    time.sleep(1)
except:
    print("Notification Recipient field not selected")

try:
    # Select Notification Assignee User/Group
    select_element = driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr[1]/td[6]/div[1]/div[1]/div[1]/select[1]")
    select = Select(select_element)
    select.select_by_visible_text(notification_assignee)
    time.sleep(1)
except:
    print("Notification Assignee User/Group not selected")
time.sleep(1)

# Scroll down by 1500 pixels
driver.execute_script("window.scrollBy(0, 1500);")
time.sleep(2)

# Select Save Option
driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()
time.sleep(1)
driver.find_element(By.XPATH, "//button[normalize-space()='OK']").click()
time.sleep(15)

# Quit Driver
driver.quit()
