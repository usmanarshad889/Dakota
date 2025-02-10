import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
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

def test_upgrade_and_configuration(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(15)

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
                select.select_by_visible_text("Create Task")
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
                select.select_by_visible_text("User")
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
    time.sleep(15)

    # Navigate to Upgrade Link
    driver.get(f"{config['base_url']}packaging/installPackage.apexp?p0=04tKf000000Y1Ew")
    time.sleep(5)

    if driver.title == "Install Package":
        print("Link is correct")

        # Click on update button
        driver.find_element(By.XPATH, "//button[@title='Upgrade']").click()
        button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
        button.click()
        time.sleep(3)

        # Navigate to installed pakages setup
        driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Setup")

        try:
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]"))
            )
            element.click()
        except:
            pass
        time.sleep(1)

        # Scroll down by 500 pixels
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(10)

        # Validate Previous configuration
        active_state = driver.find_element(By.XPATH, "//span[@class='slds-checkbox_on']")
        if active_state.text.lower() == 'active':
            assert True
        else:
            assert False

    else:
        print("Upgrade Package Link is not correct")
        driver.quit()
        assert False
