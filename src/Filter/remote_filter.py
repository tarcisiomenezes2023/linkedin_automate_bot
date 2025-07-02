import time
import random
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Remote_filter_jobs(driver):
    job_keywords = "Python" # "Excel", "programming", "frontend", "Javascript", "data", "sustainability", "environmental", "water", "air", "health and safety
    location_keyword = "European Union" 

    wait = WebDriverWait(driver, 10)

    try:
        # Job and location input
        job_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@id, "jobs-search-box-keyword-id")]')))
        location_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@id, "jobs-search-box-location-id")]')))

        job_field.clear()
        location_field.clear()

        job_field.send_keys(job_keywords)
        time.sleep(random.uniform(1.0, 5.0))
        location_field.send_keys(Keys.CONTROL + "a")
        location_field.send_keys(Keys.BACKSPACE)
        time.sleep(random.uniform(1.0, 5.0))

        job_field.send_keys(Keys.RETURN)
        time.sleep(random.uniform(3.0, 5.0))

    except Exception as e:
        print(f'❌ Error entering search terms: {e}')

    # === Filter: All filters button ===
    try:
        # Wait and locate the "All filters" button by its ID
        all_filters_btn = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show all filters. Clicking this button displays all available filter options.']"))
        )
        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView(true);", all_filters_btn)
        time.sleep(random.uniform(1.0, 3.0))
        all_filters_btn.click()
        print("✅ 'All filters' button clicked successfully!")
        time.sleep(random.uniform(1.0, 8.0))

    except Exception as e:
        print(f"⚠️ Could not apply 'All filters' filter: {e}")
        
    # === Filterings for Most recent, Past 24 hours, Internship, Easy Apply, Entry level, and Remote.
    # === Date posted: Past 24 hours ===
    try:
        date_posted_option = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//label[contains(., 'Past 24 hours')]"
        )))
        date_posted_option.click()
        print("✅ 'Past 24 hours' option selected!")

    except Exception as e:
        print(f"⚠️ Could not select 'Past 24 hours': {e}")


    # === Experience Level: Internship and Entry level ===
    try:
        internship = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//label[contains(., 'Internship')]"
        )))
        internship.click()
        time.sleep(random.uniform(1.0, 5.0))

        entry = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//label[contains(., 'Entry level')]"
        )))
        entry.click()
        print("✅ 'Internship' and 'Entry level' options selected!")

    except Exception as e:
        print(f"⚠️ Could not select 'Internship and Entry level': {e}")


    # === Remote ===
    try:
        remote_option = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//label[contains(., 'Remote')]"
        )))
        remote_option.click()
        print("✅ 'Remote' option selected!")

    except Exception as e:
        print(f"⚠️ Could not select 'Remote': {e}")
    
    # === Easy Apply toggle ===
    try:
        # 1. Localiza o input real do toggle
        easy_apply_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//input[@role='switch' and @type='checkbox' and "
                "@data-artdeco-toggle-button='true' and contains(@class,'artdeco-toggle__button')]"
            ))
        )

        # 2. Se ainda está desligado, clica via JavaScript no próprio input
        if easy_apply_input.get_attribute("aria-checked") == "false":
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", easy_apply_input)
            time.sleep(random.uniform(0.3, 0.7))

            driver.execute_script("arguments[0].click();", easy_apply_input)

            # 3. Aguarda confirmação de que mudou para 'true'
            WebDriverWait(driver, 5).until(
                lambda d: easy_apply_input.get_attribute("aria-checked") == "true"
            )
            print("✅ Easy Apply realmente ativado!")

        else:
            print("ℹ️ Easy Apply já estava ativado.")

    except Exception as e:
        print(f"⚠️ Ainda não foi possível ativar Easy Apply: {e}")

    # Apply filters:
    try:
        show_results_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'search-reusables__secondary-filters-show-results-button') and contains(., 'Show')]"
        )))

        # Scroll into view and click via JS to avoid interception
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_results_button)
        time.sleep(random.uniform(0.5, 5.0))
        driver.execute_script("arguments[0].click();", show_results_button)

        print("✅ 'Show results' clicked!")
        time.sleep(random.uniform(1.0, 5.0))

    except Exception as e:
        print(f"⚠️ Could not click 'Show results': {e}")