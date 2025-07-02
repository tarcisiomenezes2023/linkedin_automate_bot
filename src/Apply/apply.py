from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def apply_jobs(driver):
    try:
        wait = WebDriverWait(driver, 10)

        # Wait and click the next card job
        job_card = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "job-card-list__title")))
        time.sleep(random.uniform(2.0, 5.0))
        job_card.click()

        # Find "Easy Apply" to click
        easy_apply_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")))
        easy_apply_btn.click()
        print("✅ Easy Apply button clicked!")

    except Exception as e:
        print(f"⚠️ Erro ao aplicar: {str(e)}")
