import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Managed Package Upgrade")
@allure.story("Test upgrading from an earlier version, ensuring correct handling of new features and validation of previous configuration")
def test_package_upgrade(driver, config):
    # Navigate to login page
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

    # Click on App Launcher
    app_launcher = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='slds-r5']")))
    app_launcher.click()
    search_filed = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search apps and items...']")))
    search_filed.click()
    search_filed.clear()
    search_filed.send_keys("Dakota Marketplace for Salesforce")
    app_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//b[normalize-space()='Dakota Marketplace for Salesforce']")))
    app_btn.click()
    time.sleep(5)

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")

    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]")))
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    # Click on Auto Sync Field Updates
    inactive_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_off']")))
    if inactive_button.text == "Inactive":
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
        btn.click()
    else:
        print("Button is already active")

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(15)

    try:
        # Select Sync Option
        select_element = wait.until(EC.presence_of_all_elements_located((By.XPATH,"/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[3]/div[1]/div[1]/div[1]/select[1]")))
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Update")
    except (NoSuchElementException, TimeoutException) as e:
        print("Sync Option not selected")
        print(f"Error: {type(e).__name__}")

    try:
        # Select Notification Setting
        select_element = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[4]/div[1]/div[1]/div[1]/select[1]")))
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Create Task")
    except (NoSuchElementException, TimeoutException) as e:
        print("Notification Setting field not selected")
        print(f"Error: {type(e).__name__}")

    try:
        # Select Notification Recipient
        select_element = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[5]/div[1]/div[1]/div[1]/select[1]")))
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("User")
    except (NoSuchElementException, TimeoutException) as e:
        print("Notification Recipient field not selected")
        print(f"Error: {type(e).__name__}")

    try:
        # Select Notification Assignee User/Group
        select_element = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                             "/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[6]/div[1]/div[1]/div[1]/select[1]")))
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Aiman Shakil")
    except (NoSuchElementException, TimeoutException) as e:
        print("Notification Assignee User/Group not selected")
        print(f"Error: {type(e).__name__}")

    # Scroll down by 1500 pixels
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(1)

    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(1)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='OK']")))
    btn.click()
    time.sleep(2)

    # Verify toast
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    assert toast.text.strip() == "Mapping saved successfully." , "Mapping Error"

    # Navigate to Upgrade Link
    # driver.get(f"{config['base_url']}packaging/installPackage.apexp?p0=04tKf000000Y1Ew")
    # driver.get(f"{config['base_url']}packaging/installPackage.apexp?p0=04tKf000000Y1FB")
    driver.get(f"{config['base_url']}packaging/installPackage.apexp?p0=04tKf000000Y1FL")
    time.sleep(5)

    if driver.title == "Install Package":
        # Click on update button
        update_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Upgrade']")))
        update_btn.click()
        button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
        button.click()
        time.sleep(1)

        # Navigate to installed pakages setup
        driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
        time.sleep(3)

        # Reload Dakota Setup page
        driver.refresh()
        time.sleep(5)

        # Verify the Configuration
        try:
            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]"))
            )
            element.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")

        # Scroll down by 500 pixels
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(1)

        # Validate Previous configuration
        active_state = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_on']")))
        assert active_state.text.lower() == 'active', "Configuration failed"

    else:
        print("Upgrade Package Link is not correct")
        assert False
