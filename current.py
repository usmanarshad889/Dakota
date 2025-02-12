import matplotlib.colors as mcolors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/")

wait = WebDriverWait(driver, 20)
username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
username.send_keys("draftsf@draftdata.com.fuseupgrad")
password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
password.send_keys("LOWYqfakgQ8oo")
login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
login_button.click()

btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='slds-tabs_default__link'])[1]")))
print(btn.text)
print("")

xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[1]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[2]'''
all_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

for element in all_elements:
    # Get the text color in rgba format
    text_color = element.value_of_css_property("color")
    print(f"Raw RGBA Color: {text_color}")  # Debug: print the raw color value

    # Extracting RGB values (Assumes text_color is in rgba(r, g, b, a) format)
    rgba_values = text_color[5:-1].split(', ')  # Removing 'rgba(' and ')'
    print(f"RGBA Components: {rgba_values}")  # Debug: print the components

    red, green, blue = [int(value) for value in rgba_values[:3]]  # Convert to integer values

    # Convert RGBA to HEX format
    hex_color = mcolors.to_hex((red / 255, green / 255, blue / 255))  # Normalize RGB values to 0-1 range
    print(f"Text Color (HEX): {hex_color}")