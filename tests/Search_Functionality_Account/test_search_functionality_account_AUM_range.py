import time
import pytest
from selenium import webdriver
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

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_search_aum(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])

    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Navigate to Marketplace Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")
    time.sleep(15)

    # Enter AUM From
    driver.find_element(By.XPATH, "//input[@name='FROM']").send_keys("1")
    time.sleep(3)

    # Enter AUM To
    driver.find_element(By.XPATH, "//input[@name='To']").send_keys("100000")
    time.sleep(3)

    # Click on Search Button
    driver.find_element(By.XPATH,
                        "//div[@class='SearchbuttonDiv']//button[@title='Search'][normalize-space()='Search']").click()
    time.sleep(5)

    # aum element value
    aum_element = driver.find_element(By.XPATH, "(//td[@data-label='AUM'])[1]")

    # Remove the dollar sign and commas, then convert to integer
    aum_value = int(aum_element.text.replace('$', '').replace(',', ''))

    # Validate if the value is within the range
    if 1 <= aum_value <= 100000:
        assert True
    else:
        assert False