import time
import random
import string
import pytest
import allure
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

value_src = "u"

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
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Mapping - Account field Mapping")
@allure.story("Validate successful mapping of account fields.")
def test_account_record_auto_sync(driver, config):
    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["uat_username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["uat_password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()

    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Account button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.standard-Account']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)

    # Move to account Tab and click on new button
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='profileTrigger branding-user-profile bgimg slds-avatar slds-avatar_profile-image-small circular forceEntityIcon']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log Out']")))
    btn.click()
    time.sleep(2)







    # Navigate to login page of fuse app
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()

    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    retries = 5
    for attempt in range(retries):
        try:
            driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
            break  # Exit the loop if the page loads successfully
        except TimeoutException:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(5)  # Wait before retrying
    else:
        print("All retry attempts failed.")
    time.sleep(2)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='profileTrigger branding-user-profile bgimg slds-avatar slds-avatar_profile-image-small circular forceEntityIcon']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log Out']")))
    btn.click()
    time.sleep(2)







    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["uat_username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["uat_password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()

    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Account button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.standard-Account']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)

    # Move to account Tab and click on new button
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='profileTrigger branding-user-profile bgimg slds-avatar slds-avatar_profile-image-small circular forceEntityIcon']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log Out']")))
    btn.click()
    time.sleep(2)








    # Navigate to login page of fuse app
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()

    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    retries = 5
    for attempt in range(retries):
        try:
            driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
            break  # Exit the loop if the page loads successfully
        except TimeoutException:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(5)  # Wait before retrying
    else:
        print("All retry attempts failed.")
    time.sleep(2)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='profileTrigger branding-user-profile bgimg slds-avatar slds-avatar_profile-image-small circular forceEntityIcon']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log Out']")))
    btn.click()
    time.sleep(2)











    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["uat_username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["uat_password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()

    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Account button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.standard-Account']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)

    # Move to account Tab and click on new button
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='profileTrigger branding-user-profile bgimg slds-avatar slds-avatar_profile-image-small circular forceEntityIcon']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log Out']")))
    btn.click()
    time.sleep(2)









    # Navigate to login page of fuse app
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()

    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    retries = 5
    for attempt in range(retries):
        try:
            driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
            break  # Exit the loop if the page loads successfully
        except TimeoutException:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(5)  # Wait before retrying
    else:
        print("All retry attempts failed.")
    time.sleep(2)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='profileTrigger branding-user-profile bgimg slds-avatar slds-avatar_profile-image-small circular forceEntityIcon']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Log Out']")))
    btn.click()
    time.sleep(2)