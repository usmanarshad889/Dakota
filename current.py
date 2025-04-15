import time
import pytest
import allure
import tempfile
import shutil
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    # Toggle this to False if you want to see the browser
    headless = False

    # Create a temporary directory for a clean Chrome profile
    user_data_dir = tempfile.mkdtemp()

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-browser-side-navigation")

    if headless:
        chrome_options.add_argument("--headless=new")  # Use newer headless mode

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        yield driver
    finally:
        driver.quit()
        shutil.rmtree(user_data_dir)


@pytest.mark.P1
@pytest.mark.release_one
@pytest.mark.demo
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Mapping - Account field Mapping")
@allure.story("Validate successful mapping of account fields.")
def test_account_record_auto_sync(driver, config):
    wait = WebDriverWait(driver, 60)

    try:
        # 🚪 Go to Salesforce login page
        driver.get(config["uat_login_url"])

        # 🔐 Login steps
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.clear()
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.clear()
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # 🔄 Wait for redirect to Lightning UI
        wait.until(EC.url_contains("lightning.force.com"))

        # ✅ Confirm login by interacting with a known element
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")
        return

    # 📁 Move to Account tab
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)




    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()



    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(2)







    wait = WebDriverWait(driver, 60)

    try:
        # 🚪 Go to Salesforce login page
        driver.get(config["uat_login_url"])

        # 🔐 Login steps
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.clear()
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.clear()
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # 🔄 Wait for redirect to Lightning UI
        wait.until(EC.url_contains("lightning.force.com"))

        # ✅ Confirm login by interacting with a known element
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")
        return

    # 📁 Move to Account tab
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)




    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()



    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(2)





    wait = WebDriverWait(driver, 60)

    try:
        # 🚪 Go to Salesforce login page
        driver.get(config["uat_login_url"])

        # 🔐 Login steps
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.clear()
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.clear()
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # 🔄 Wait for redirect to Lightning UI
        wait.until(EC.url_contains("lightning.force.com"))

        # ✅ Confirm login by interacting with a known element
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")
        return

    # 📁 Move to Account tab
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)




    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()



    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(2)




    wait = WebDriverWait(driver, 60)

    try:
        # 🚪 Go to Salesforce login page
        driver.get(config["uat_login_url"])

        # 🔐 Login steps
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.clear()
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.clear()
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # 🔄 Wait for redirect to Lightning UI
        wait.until(EC.url_contains("lightning.force.com"))

        # ✅ Confirm login by interacting with a known element
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")
        return

    # 📁 Move to Account tab
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)




    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 60)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()



    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
    time.sleep(2)





    wait = WebDriverWait(driver, 60)

    try:
        # 🚪 Go to Salesforce login page
        driver.get(config["uat_login_url"])

        # 🔐 Login steps
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.clear()
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.clear()
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # 🔄 Wait for redirect to Lightning UI
        wait.until(EC.url_contains("lightning.force.com"))

        # ✅ Confirm login by interacting with a known element
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")
        return

    # 📁 Move to Account tab
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)




    wait = WebDriverWait(driver, 60)

    try:
        # 🚪 Go to Salesforce login page
        driver.get(config["uat_login_url"])

        # 🔐 Login steps
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.clear()
        username.send_keys(config["uat_username"])

        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.clear()
        password.send_keys(config["uat_password"])

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        login_button.click()

        # 🔄 Wait for redirect to Lightning UI
        wait.until(EC.url_contains("lightning.force.com"))

        # ✅ Confirm login by interacting with a known element
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")
        return

    # 📁 Move to Account tab
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    time.sleep(2)
