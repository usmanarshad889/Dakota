import time
import random
import string
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

field_name = "Automation " + ''.join(random.choices(string.ascii_uppercase, k=3))
print(field_name)

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Field Display")
@allure.story("Validate that the newly added field is displayed correctly in the preview popup.")
def test_field_preview_display(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
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
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

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


    # Navigate to account's object field and relationship page
    package_url = f"{config['base_url']}lightning/setup/ObjectManager/Account/FieldsAndRelationships/view"
    driver.get(package_url)

    # Click on New button
    btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Custom Field']")))
    time.sleep(1)
    btn.click()

    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Account: New Custom Field ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # Scroll down in iframe
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[1]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Lookup Relationship']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Date/Time']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Phone']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

    # Click on Text field radio button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='dtypeS']")))
    btn.click()

    # scroll up
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[1]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Next']")))
    btn.click()

    # Enter Field Label
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MasterLabel']")))
    btn.send_keys(field_name)

    # Enter length
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Length']")))
    btn.send_keys("35")

    # Enter Description
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='Description']")))
    btn.send_keys("This is Automation field description created by Selenium Python")

    # Enter Help Text
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='InlineHelpText']")))
    btn.send_keys("Automation Test")

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Next']")))
    btn.click()

    # Click on Visible checkbox
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@title='Visible'])")))
    btn.click()

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Next']")))
    btn.click()

    # Click on Save button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Save']")))
    btn.click()

    # Switch out of iframe
    driver.switch_to.default_content()
    time.sleep(1)

    # Verify the field creation
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='globalQuickfind']")))
    btn.send_keys(field_name)
    time.sleep(4)

    # Extract field context
    actual_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//tr//td[1]")))
    print(f"Actual field Text : {actual_field.text}")

    assert actual_field.text == field_name , f"Expected field was {field_name} but got {actual_field.text}"
    time.sleep(1)

    # Navigate to Account Tab in Dakota Marketplace
    package_url = f"{config['base_url']}lightning/o/Account/list?filterName=__Recent"
    driver.get(package_url)

    # Click on new button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    time.sleep(1)
    btn.click()

    # Click on next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
    time.sleep(1)
    btn.click()

    # Scroll down
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='SEC Registered Date']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='NAIC Number']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Chicago Pacific PM Call')]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)

    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='QA Text (10)']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)
    time.sleep(1)


    # Verify the new field
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space()='{field_name}']")))
    text_field = btn.text
    print(f"Field Text : {text_field}")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    assert text_field == field_name , f"Expected field not displayed"
    time.sleep(1)


    # Navigate to account's object field and relationship page
    package_url = f"{config['base_url']}lightning/setup/ObjectManager/Account/FieldsAndRelationships/view"
    driver.get(package_url)


    # Delete the field created
    btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='globalQuickfind']")))
    btn.send_keys(field_name)
    time.sleep(4)

    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='rowActionsPlaceHolder slds-button slds-button--icon-border-filled']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Delete']//div[@class='slds-grid']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'label bBody')][normalize-space()='Delete']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(5)