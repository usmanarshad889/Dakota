import time
import random
import string
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

picklist_name = "Automation Testing " + ''.join(random.choices(string.ascii_uppercase, k=3))
print(picklist_name)


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_four
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Picklist Values")
@allure.story("Confirm picklist value deactivation functionality.")
@pytest.mark.all
@pass_broken
def test_picklist_value_addition_to_account_field_type(driver, config):
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


    # Navigate to contact's object field and relationship page
    package_url = f"{config['base_url']}lightning/setup/ObjectManager/Contact/FieldsAndRelationships/view"
    driver.get(package_url)


    # Search Dakota Contact Type
    btn = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='globalQuickfind']")))
    time.sleep(2)
    btn.send_keys("Dakota Contact Type")
    time.sleep(5)


    # Click on the Dakota Contact Type button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Dakota Contact Type']")))
    btn.click()


    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Contact Custom Field: Dakota Contact Type ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # Scrolldown in iframe
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Data Sensitivity Level']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(text(),'Restrict picklist to the values defined in the val')]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[@id='ValidationFormulaList_title']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[normalize-space()='Values']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='New Values']")))
    btn.click()
    driver.switch_to.default_content()
    time.sleep(1)


    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Add Picklist Values: Dakota Contact Type ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)


    # Add a Picklist Value
    value = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@title='Dakota Contact Type']")))
    value.send_keys(picklist_name)


    # Scroll down
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@title='Dakota Contact Type']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)
    time.sleep(1)


    # Click on Record Type Name Checkbox
    check_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='allBox']")))
    check_box.click()


    # Click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@title='Save']")))
    save_btn.click()
    driver.switch_to.default_content()
    time.sleep(1)


    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Contact Custom Field: Dakota Contact Type ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # Scrolldown in iframe
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[normalize-space()='Data Sensitivity Level']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//td[contains(text(),'Restrict picklist to the values defined in the val')]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[@id='ValidationFormulaList_title']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[normalize-space()='Values']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)


    # Verify added picklist value
    all_picklist_values = driver.find_elements(By.XPATH, "//th[@class=' dataCell  ']")

    # Assert that picklist values exist
    assert all_picklist_values, "No picklist values found."

    picklist_found = False
    for picklist_value in all_picklist_values:
        picklist_value_text = picklist_value.text.strip()
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", picklist_value)

        if picklist_value_text == picklist_name:
            time.sleep(2)  # Use explicit wait instead in real scenarios
            picklist_found = True
            allure.attach(f"Picklist value '{picklist_name}' found and clicked.", name="Picklist Verification")
            break

    assert picklist_found, f"Picklist value '{picklist_name}' not found."

    rows = driver.find_elements(By.XPATH,
                                "/html[1]/body[1]/div[8]/div[1]/div[1]/form[1]/div[2]/table[1]/tbody[1]/tr/th[1]")
    target_name = picklist_name

    for index, row in enumerate(rows, start=1):  # Loop through each row
        try:
            # Construct dynamic XPath for the name in the current row
            name_xpath = f"/html[1]/body[1]/div[8]/div[1]/div[1]/form[1]/div[2]/table[1]/tbody[1]/tr[{index}]/th[1]"
            name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, name_xpath))
            )
            print(f"{index}, {name_element.text}")

            if name_element.text.strip() == target_name:
                print(f"Element found: {name_element.text.strip()}")

                # Construct XPath for the element to click in the same row
                element_xpath = f"/html[1]/body[1]/div[8]/div[1]/div[1]/form[1]/div[2]/table[1]/tbody[1]/tr[{index}]/td[1]/a[3]"
                another_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, element_xpath))
                )

                another_element.click()
                time.sleep(2)
                alert = driver.switch_to.alert  # Switch to alert
                alert.accept()  # Accept the alert (or use alert.dismiss() to cancel)
                print("Alert accepted")
                driver.switch_to.default_content()
                break  # Exit loop once found
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")
    time.sleep(6)
