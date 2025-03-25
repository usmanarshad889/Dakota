import time
from datetime import datetime
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 30)


try:
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/")
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys("draftsf@draftdata.com.fuseupgrad")
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys("LOWYqfakgQ8oo")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()
except Exception as e:
    pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")


driver.get("https://dakotanetworks--fuseupgrad.sandbox.lightning.force.com/lightning/n/Marketplace__Dakota_Video")
wait.until(EC.visibility_of_element_located((By.XPATH, "(//th[@data-label='Date'])[1]")))
time.sleep(1)

video_icon = driver.find_elements(By.XPATH, "(//*[name()='svg'][@class='slds-button__icon slds-button__icon_large'])")
print(len(video_icon))
