import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Path for the chrome profile
PROFILE_PATH = os.path.abspath("chrome_profile")
options = Options()
options.add_argument(f"--user-data-dir={PROFILE_PATH}")
options.add_argument("--disable-notifications")
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

# Load credentials
username = "tarcisiomenezes2019@hotmail.com"
password = "Virus1703?"

# Initialize web browser with persistent profile
driver = webdriver.Chrome(options=options)  # ✅ aqui passa as opções
driver.get("https://www.linkedin.com/login/")

# Wait like a human
time.sleep(random.uniform(2.0, 8.0))

try:
    # Fill login form
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    for char in username:
        username_field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

    time.sleep(random.uniform(1.0, 2.0))

    for char in password:
        password_field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))

    time.sleep(random.uniform(1.0, 2.0))

    sign_in_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Sign in"]')
    sign_in_button.click()

    # Simulate scroll like a human
    time.sleep(random.uniform(5.0, 7.0))
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(random.uniform(1.5, 3.0))

except NoSuchElementException:
    print("Já está logado - campos de login nao serao encontrados.")

print("✅ SUCCESS!")