from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def simulate_human_behavior(driver):
    # Scroll like human
    try:
        time.sleep(random.uniform(5.0, 7.0))
        driver.execute_script("window.scrollTo(0, 2000);")
        time.sleep(random.uniform(1.5, 3.0))
    except Exception as e:
        print(f'ERROR to scroll feed: {e}')
        
    # Button for Notifications
    try:
        notifications_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/notifications/")]'))
        )
        notifications_button.click()
        time.sleep(random.uniform(5, 15))
        print("✅ Botão de Notificações clicado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao clicar no botão de Notificações: {e}")

    # Button for job page
    try:
        jobs_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/jobs/")]'))
        )
        jobs_button.click()
        time.sleep(random.uniform(3, 10))
        print("✅ Botão de Vagas clicado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao clicar no botão de Vagas: {e}")
