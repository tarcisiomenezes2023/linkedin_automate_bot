from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def apply_jobs(driver):
    try:
        wait = WebDriverWait(driver, 10)

        # 1️⃣  Espera o botão ficar clicável
        apply_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@id='jobs-apply-button-id' and contains(., 'Easy Apply')]"
        )))

        # 2️⃣  Garante que está no viewport
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", apply_button)
        time.sleep(random.uniform(0.3, 1.0))

        # 3️⃣  Clica via JavaScript
        driver.execute_script("arguments[0].click();", apply_button)
        print("✅ Botão 'Easy Apply' clicado com sucesso!")

    except Exception as e:
        print(f"⚠️ ERRO: não foi possível clicar no botão 'Easy Apply': {e}")
