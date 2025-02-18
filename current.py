import time
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

btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
btn.click()

btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
btn.click()

btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @placeholder='Search People...']")))
btn.click()
btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//records-record-layout-lookup[@data-input-element-id='input-field']//li[2]")))
btn.click()

element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='postalCode']")))
driver.execute_script("arguments[0].scrollIntoView();", element)


element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='LinkedIn_URL__c']")))
driver.execute_script("arguments[0].scrollIntoView();", element)
time.sleep(1)


btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Accounts...']")))
btn.click()
btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='slds-grid slds-size_1-of-1 label-stacked']//records-record-layout-lookup[@data-input-element-id='input-field']//li[2]")))
print(btn.text)
btn.click()