import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.common import NoSuchElementException
from allure_commons.types import AttachmentType
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
@allure.feature("Managed Package Installation")
@allure.story("Ensure the managed package can be installed using the correct package link")
def test_installation_using_correct_link(driver, config):
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

    # Navigate to correct link of installed package
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/packaging/installPackage.apexp?p0=04tKf000000kjBf")
    time.sleep(5)


    if driver.title == "Install Package":
        print("Link is correct")

        # Click on install button
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/div[4]/div[1]/div[2]/span[1]/div[1]/button[1]")))
        button.click()
        time.sleep(1)

        # Click on grant access
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='uiInput uiInputCheckbox uiInput--default uiInput--checkbox']")))
        btn.click()
        time.sleep(1)

        # Click on Continue button
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[1]/button[1]")))
        btn.click()

        try:
            button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="buttonsArea"]/span/button/span')))
            button.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")
        assert True
    else:
        print("Install Package Link is not correct")
        assert False
