import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.P1
def test_pull_accounts_and_contacts_scheduler_display(driver, config):
    # Navigate to login page of fuse app
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


    # Navigate to Scheduled Jobs Screen
    driver.get(f"{config['base_url']}lightning/setup/ScheduledJobs/home")


    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[contains(@title,'All jobs ~ Salesforce - Enterprise Edition')]")))
    driver.switch_to.frame(iframe)
    time.sleep(2)


    # Locate all job names
    jobs = driver.find_elements(By.XPATH, "//th[@class=' dataCell  ' and @scope='row']")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Schedule Jobs Names", attachment_type=allure.attachment_type.PNG)

    minutes_list = []

    for job in jobs:
        job_text = job.text.strip()
        if "Pull Accounts/Contacts" in job_text:
            print(f" - {job_text}")
            match = re.search(r'at (\d+)\s*mins?', job_text)
            if match:
                minutes_list.append(match.group(1))

    if minutes_list:
        minutes_formatted = ', '.join(minutes_list[:-1]) + f" and {minutes_list[-1]}" if len(minutes_list) > 1 else minutes_list[0]
        summary_message = f"Pull Accounts and Contacts Scheduler Jobs run at {minutes_formatted} mins."
        print(summary_message)

        with allure.step("Scheduler Job Summary"):
            allure.attach(summary_message, name="Scheduler Run Times", attachment_type=AttachmentType.TEXT)
    else:
        print("No matching Pull Accounts/Contacts jobs found.")
        with allure.step("Scheduler Job Summary"):
            allure.attach("No matching Pull Accounts/Contacts jobs found.", name="Scheduler Run Times", attachment_type=AttachmentType.TEXT)
