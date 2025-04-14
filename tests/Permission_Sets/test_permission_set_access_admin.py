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


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Permission Sets")
@allure.story("Ensure permission sets Admin restrict or grant access as expected.")
def test_permission_set_admin(driver, config):
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


    # Navigate to installed package Page
    package_url = f"{config['base_url']}lightning/setup/PermSets/home"
    driver.get(package_url)

    # Verify page title
    try:
        expected_title = "Lightning Experience"
        actual_title = driver.title
        assert actual_title == expected_title, f"Page title mismatch: Expected '{expected_title}', but got '{actual_title}'"
    except Exception as e:
        pytest.fail(f"Title Verification Failed: {e}")

    try:
        # Locate and switch to the iframe
        iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Permission Sets ~ Salesforce - Enterprise Edition']")))
        driver.switch_to.frame(iframe_element)
        time.sleep(1)
        print(f"Successfully switched to {iframe_element.text} iframe")
    except Exception as e:
        print(str(e).split(":")[0])

    try:
        # Verify the Admin User Permission Set presence ?
        xpath = '''/html[1]/body[1]/div[3]/div[1]/form[1]/div[3]/div[4]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div/table/tbody/tr/td[4]/div/a/span'''
        all_permission = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        permission_found = False

        for permission in all_permission:
            if permission.text.strip() == "Dakota Marketplace Admin":
                print(f"{permission.text} is present")
                permission.click()
                permission_found = True
                break

        if not permission_found:
            print("Test case failed due to absence of 'Dakota Marketplace Admin' permission")
            driver.quit()
    except Exception as e:
        print(str(e).split(":")[0])
        driver.quit()

    # Switched out of iframe
    driver.switch_to.default_content()
    time.sleep(1)


    try:
        # Switch to iframe
        iframe_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Permission Set: Dakota Marketplace Admin ~ Salesforce - Enterprise Edition']")))
        driver.switch_to.frame(iframe_element)
        time.sleep(1)
        print(f"Successfully switched to {iframe_element.text} iframe")
    except Exception as e:
        print(str(e).split(":")[1])

    try:
        # Click on Manage Assignment button
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='page:console:pc_form:button_manage_assignments']")))
        btn.click()
    except Exception as e:
        print(str(e).split(":")[1])
    # Switched out of iframe
    driver.switch_to.default_content()
    time.sleep(1)

    try:
        # Click on Add Assignment button
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add Assignment']")))
        btn.click()
    except Exception as e:
        print(str(e).split(":")[1])

    try:
        # Store the current username
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='uiImage'])[1]")))
        btn.click()
        profile_name = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='profile-link-label'])[1]"))).text
        driver.find_element(By.XPATH, "//button[@title='Close']//lightning-primitive-icon[@variant='bare']").click()

        # Enter and Search the UserName
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='User-search-input']")))
        btn.send_keys(profile_name)
        driver.find_element(By.XPATH, "//button[@title='Refresh']//lightning-primitive-icon[@exportparts='icon']").click()
        time.sleep(5)
    except Exception as e:
        print(str(e).split(":")[1])


    try:
        # Add Searched user and click on NEXT button
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox--faux slds-checkbox_faux'])[2]")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Next']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Assign']")))
        btn.click()
    except Exception as e:
        print(str(e).split(":")[1])

    # Verify the Result
    status = wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-formatted-text[@class='slds-m-left_x-small']")))
    expected_status = "Success"
    actual_status = status.text
    driver.find_element(By.XPATH, "//button[normalize-space()='Done']").click()

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    if actual_status == expected_status:
        print(f"Status Detail: {actual_status}")
        assert True
    else:
        print(f"Status Detail: {actual_status}")
        assert False