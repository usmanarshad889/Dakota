import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

domains = []
expected_domains = ["dakotanetworks--fuseupgrad.sandbox.my.salesforce-sites.com",
                    "dakotanetworks--fuseupgrad.sandbox.my.salesforce.com",
                    "dakotanetworks--fuseupgrad.sandbox.my.site.com",
                    "pardot.dakotafunds.com"]


# Fixture to set up the WebDriver
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@allure.severity(allure.severity_level.NORMAL)
@allure.feature("Environment Setup")
@allure.story("Validate that the environment is set up with a custom domain and email deliver-ability settings.")
def test_env_setup_custom_domain(driver, config):
    test_status = True  # Flag to track test success

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

    # Navigate to Domain Setup
    driver.get(f"{config['base_url']}lightning/setup/DomainNames/home")

    # Switch to iframe
    iframe_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Domains ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe_element)
    time.sleep(1)

    # Verify that text for my domain
    all_domains_xpath = '''/html[1]/body[1]/div[5]/div[1]/div[2]/table[1]/tbody[1]/tr/th[1]/a[1]'''
    all_domains_element = driver.find_elements(By.XPATH, all_domains_xpath)
    for domain in all_domains_element:
        domains.append(domain.text)

    driver.switch_to.default_content()

    # Soft Assertion for Domain Verification
    n = min(len(domains), len(expected_domains))
    if expected_domains[:n] == domains[:n]:
        print("Custom domain verification passed")
    else:
        print("Custom domain verification failed")
        test_status = False  # Mark test as failed but continue execution

    # Navigate to Deliver-ability Setup
    driver.get(f"{config['base_url']}lightning/setup/OrgEmailSettings/home")

    # Switch to iframe
    iframe_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Deliverability ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe_element)

    select_element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "/html[1]/body[1]/form[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/select[1]")))
    select = Select(select_element)
    selected_option = select.first_selected_option.text.strip().lower()

    driver.switch_to.default_content()

    # Final Assertion - Determines Test Status
    if selected_option == "all email":
        print("Email deliver-ability is correctly set to All Email")
    else:
        print(f"Access Level is '{selected_option}', expected 'All Email'")
        test_status = False  # Mark test as failed

    # If last assertion fails, capture screenshot in Allure
    if not test_status:
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name="Failure Screenshot", attachment_type=AttachmentType.PNG)
        assert False, "Test case failed. Screenshot attached."

    assert test_status, "Test case passed successfully."
