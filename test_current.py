import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and quit WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_package_installation(driver, config):
    wait = WebDriverWait(driver, 20)
    driver.get(config["base_url"])

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()
    except Exception as e:
        pytest.fail(f"Login failed: {e}")

    # Navigate to Installed Packages page
    installed_packages_url = f"{config['base_url']}lightning/setup/ImportedPackage/home"
    driver.get(installed_packages_url)

    try:
        # Wait for iframe and switch to it
        iframe_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//iframe[@title='Installed Packages ~ Salesforce - Enterprise Edition']")
        ))
        driver.switch_to.frame(iframe_element)

        # Wait for package table to load
        packages = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "/html/body/div[3]/div[1]/div[1]/div[2]/table/tbody/tr/th/a")
        ))

        # Check if "Dakota Marketplace for Salesforce" exists
        package_names = [package.text.strip().lower() for package in packages]
        assert "dakota marketplace for salesforce" in package_names, "Dakota package is NOT installed."

        print("Dakota Package Present")  # You can replace this with logging if needed.

    except Exception as e:
        pytest.fail(f"Error finding installed packages: {e}")

    finally:
        # Switch back to the default content
        driver.switch_to.default_content()
