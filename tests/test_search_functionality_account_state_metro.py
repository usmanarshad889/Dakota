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

def test_search_state_metro_area(driver, config):
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
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Search")
    time.sleep(15)

    # Select New York from filter
    button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[1]//div[4]//div[1]//div[2]//div[1]//div[1]//div[1]//input[1]")))
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

    driver.find_element(By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[1]").send_keys("New York City")
    time.sleep(2)

    button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[1]//div[4]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li[258]//div[1]")))
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)

    # Select State filter
    state = driver.find_element(By.XPATH, "//input[contains(@placeholder,'Select State(s)')]")
    state.click()
    time.sleep(1)
    state_name = driver.find_element(By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[3]")
    state_name.send_keys("New York")
    time.sleep(2)
    driver.find_element(By.XPATH,
                        "//div[6]//div[1]//div[2]//div[1]//div[1]//div[2]//ul[1]//div[1]//li[42]//div[1]").click()
    time.sleep(2)

    # click on search button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    button.click()
    time.sleep(10)

    # Verify the search result
    actual_state = driver.find_element(By.XPATH, "(//td[contains(@data-label,'State')])[1]").text
    actual_metro_area = driver.find_element(By.XPATH, "(//td[contains(@data-label,'Metro Area')])[1]").text
    # print(actual_state.lower())
    # print(actual_metro_area.lower())

    if actual_state.lower() == "ny" and actual_metro_area.lower() == "new york city":
        assert True
    else:
        assert False