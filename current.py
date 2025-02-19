import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/")

wait = WebDriverWait(driver, 20)
username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
username.send_keys("draftsf@draftdata.com.uat")
password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
password.send_keys("Rolustech@99")
login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
login_button.click()

driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/lightning/o/Contact/list?filterName=00BWF0000006vQD2AY")

API_URL = "https://dakotanetworks--uat.sandbox.li\ui-instrumentation-components-beacon.InstrumentationBeacon.sendData=1"  # Replace with actual API URL

"""Check API status and return True if it's up, False otherwise"""
try:
    response = requests.get(API_URL, timeout=20)
    if response.status_code == 200:
        print("✅ API is UP!")
    else:
        print(f"❌ API is DOWN! Status Code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"❌ API check failed: {e}")
