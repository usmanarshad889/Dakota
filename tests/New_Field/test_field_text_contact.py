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

def test_field_text(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    try:
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()
    except Exception as e:
        pytest.fail(f"Login failed: {e}")


    # Navigate to account's object field and relationship page
    package_url = f"{config['base_url']}lightning/setup/ObjectManager/Contact/FieldsAndRelationships/view"
    driver.get(package_url)

    # Click on New button
    btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Custom Field']")))
    time.sleep(1)
    btn.click()

    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Contact: New Custom Field ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # Scrolldown in iframe
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

    # Extraxt field context
    actual_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//tr//td[1]")))
    print(f"Actual field Text : {actual_field.text}")

    assert actual_field.text == field_name , f"Expected field was {field_name} but got {actual_field.text}"
    time.sleep(1)


    #Click on new field
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//body[1]/div[4]/div[1]/section[1]/div[1]/div[1]/div[2]/div[2]/section[2]/div[1]/div[1]/section[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/section[1]/div[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/a[1]")))
    btn.click()

    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, f"//iframe[@title='Contact Custom Field: {field_name} ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # Verify the text type
    text = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Text']"))).text
    print(f"Actual Text Type : {text}")

    assert text == "Text" , f"Expected Data Type was 'Text' but got {text}"
    time.sleep(1)

    driver.switch_to.default_content()
    driver.back()


    # Delete the field created
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='globalQuickfind']")))
    btn.send_keys(field_name)
    time.sleep(4)

    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='rowActionsPlaceHolder slds-button slds-button--icon-border-filled']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Delete']//div[@class='slds-grid']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'label bBody')][normalize-space()='Delete']")))
        btn.click()
        time.sleep(5)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")