import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_six
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Package Installation")
@allure.story("Confirm the package shows install users as: Admin only, All users, Specific profiles.")
def test_package_install_users(driver, config):
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
    driver.get(f"{config['base_url']}packaging/installPackage.apexp?p0=04tKf000000kjBf")
    time.sleep(5)

    if driver.title == "Install Package":
        print("Link is correct")
    else:
        print("Link is not correct and unable to test the testcase")
        assert False

    #  Copy All users text
    admin_user = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Install for Admins Only')]")))
    all_user = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Install for All Users')]")))
    specific_user = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Install for Specific Profiles...')]")))

    # Verify users
    if admin_user.text.lower() == "install for admins only" and all_user.text.lower() == "install for all users" and specific_user.text.lower() == "install for specific profiles...":
        print("Package can be install for following users ...\n")
        print(f"1. {admin_user.text}")
        print(f"2. {all_user.text}")
        print(f"3. {specific_user.text}")
        assert True

    else:
        print("Test Case Fail")
        assert False