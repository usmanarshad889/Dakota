import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
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

def test_non_admin_user_permission_set(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)


    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(2)


    # Navigate to installed package Page
    package_url = f"{config['base_url']}lightning/setup/ManageUsers/home"
    driver.get(package_url)


    # Locate and switch to the iframe
    iframe_element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//iframe[contains(@title, 'Salesforce - Enterprise Edition')]")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)


    # Select Active Users in the dropdown
    dropdown_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='fcf']")))
    options = Select(dropdown_field)
    options.select_by_visible_text("Active Users")

    # Locate All Active Users
    xpath = '''/html[1]/body[1]/div[5]/div[1]/form[1]/div[2]/table[1]/tbody[1]/tr/th[1]/a[1]'''
    all_users = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Locate 'Shakil, Aiman' user in for loop
    for user in all_users:
        user_text = user.text.strip()
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", user)
        if user_text == "Shakil, Aiman":
            user.click()
            break

    driver.switch_to.default_content()
    time.sleep(1)


    # Locate and switch to the iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[contains(@title,'User: Aiman Shakil ~ Salesforce - Enterprise Edition')]")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)


    # Scrolldown to element
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Locale']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Last Login']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Created By']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)
    time.sleep(1)


    # Click on Edit Assignments
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@title,'Edit Assignments')])[1]")))
    btn.click()
    driver.switch_to.default_content()
    time.sleep(1)


    # Locate and switch to the iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Permission Set Assignments: Aiman Shakil ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)


    # Select Permission Sets in the dropdown
    dropdown_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='thePage:theForm:thePageBlock:permSetAssignSection:pages:duelingListBox:backingList_a']")))
    options = Select(dropdown_field)
    options.select_by_visible_text("13F Filings Permissions")


    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@id='thePage:theForm:thePageBlock:permSetAssignSection:pages:duelingListBox:add']")))
    btn.click()

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@value='Save'])[2]")))
    btn.click()
    driver.switch_to.default_content()

    # Verify the Permission Set
    # Locate and switch to the iframe
    iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[contains(@title,'User: Aiman Shakil ~ Salesforce - Enterprise Edition')]")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)


    # Scrolldown to element
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Locale']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Last Login']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Created By']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@title,'Edit Assignments')])[1]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
    time.sleep(1)


    # Verify the added permission set
    permission_name = driver.find_element(By.XPATH, "//a[normalize-space()='13F Filings Permissions']")
    assert permission_name.text.strip() == "13F Filings Permissions" , "Permission Set not added"

    # Delete the permission set
    del_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Delete - Record 1 - 13F Filings Permissions']")))
    del_btn.click()
    time.sleep(1)

    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(5)
