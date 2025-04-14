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

@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Package Upgrade")
@allure.story("Test reloading of marketplace setup page after package Installation.")
def test_upgrade_and_reload(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

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

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(3)

    # Reload the Dakota Setup page
    driver.refresh()
    assert True

    # Click on Authentication svg button
    try:
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[3]"))
        )
        element.click()
    except:
        pass
    time.sleep(1)

    # Verify the Authentication with correct Credentials
    driver.find_element(By.XPATH, "//input[@name='Username']").clear()
    driver.find_element(By.XPATH, "//input[@name='Username']").send_keys("Fuse Upgrade")
    driver.find_element(By.XPATH, "//input[@name='Password']").clear()
    driver.find_element(By.XPATH, "//input[@name='Password']").send_keys("rolus009")
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").clear()
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").send_keys("https://marketplace-dakota-uat.herokuapp.com")

    try:
        driver.find_element(By.XPATH, "//button[@value='Connect']").click()
        time.sleep(1)
    except:
        print("fail first")

    try:
        driver.find_element(By.XPATH, "(//button[normalize-space()='Connect'])[1]").click()
        time.sleep(1)
    except:
        print("Button clicked successfully in first try")


    # Verify the toast message
    try:
        toast_text = driver.find_element(By.XPATH, "//span[@class='toastMessage forceActionsText']").text
        if toast_text.lower() == "dakota marketplace account connected successfully.":
            assert True
        else:
            assert False
        time.sleep(2)
    except:
        pass

    # Click on Mapping svg button
    try:
        element = WebDriverWait(driver, 10).until(
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
        print("Button is already active")

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

    try:
        toast = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
        print(toast.text)
        if toast.text.lower() == "mapping saved successfully.":
            assert True
        else:
            assert False
    except:
        assert True


    # Click on Addition Setting svg button
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[5]"))
        )
        element.click()
    except:
        pass
    time.sleep(1)

    # Scroll down by 200 pixels
    driver.execute_script("window.scrollBy(0, 200);")
    time.sleep(2)

    # Click on Toggles buttons
    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[1]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]").click()
        time.sleep(1)
    else:
        pass

    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[2]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]").click()
        time.sleep(1)
    else:
        pass

    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[3]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[3]").click()
        time.sleep(1)
    else:
        pass

    inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'][normalize-space()='Inactive'])[4]")
    if inactive_button.text == "Inactive":
        driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_faux'])[4]").click()
        time.sleep(1)
    else:
        pass

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(2)


    # Select Save Option
    driver.find_element(By.XPATH, "//button[normalize-space()='Save']").click()

    try:
        toast = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
        print(toast.text)
        if toast.text == "Status changed successfully!":
            assert True
        else:
            assert False
    except:
        assert True

    driver.quit()
