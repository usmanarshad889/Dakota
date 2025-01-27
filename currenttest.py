import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_package = []

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

# Open the Salesforce URL
driver.get("https://dakotanetworks--sand2024.sandbox.lightning.force.com/lightning/n/Marketplace__Investments")

# Log in
wait = WebDriverWait(driver, 10)
username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
username.clear()
username.send_keys("draftsf@draftdata.com.sand2024")

password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
password.clear()
password.send_keys("LOWYqfakgQ8oo")

login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
login_button.click()

# Wait for page to load
time.sleep(5)


# Navigate to installed pakages setup
driver.get("https://dakotanetworks--sand2024.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Setup")
time.sleep(15)

try:
    # Using class name (if applicable)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]"))
    )
    element.click()
    print("Clicked using CLASS_NAME")

except Exception as e:
    print("Failed to click using CLASS_NAME. Error:", e)
time.sleep(1)
driver.find_element(By.XPATH, "//span[@class='slds-checkbox_faux']").click()
time.sleep(1)

