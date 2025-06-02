import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def filter_jobs(driver):
    wait = WebDriverWait(driver, 10)
    job_keywords = ["Python", "Excel", "sustainability"]
    location_keywords = ["Budapest", "European Union"]

    for job in job_keywords:
        for location in location_keywords:
            print(f"\n🔍 Searching: {job} | Location: {location}")
            try:
                driver.get("https://www.linkedin.com/jobs/")
                time.sleep(3)

                # Enter job keyword
                job_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[aria-label="Search jobs"]')))
                job_input.clear()
                job_input.send_keys(job)
                time.sleep(1)

                # Enter location
                location_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search location"]')
                location_input.clear()
                location_input.send_keys(location)
                time.sleep(1)

                # Click Search
                search_btn = driver.find_element(By.XPATH, '//button[@data-tracking-control-name="public_jobs_jobs-search-bar_base-search-bar-search-submit"]')
                search_btn.click()
                time.sleep(3)

                # Click "All filters"
                all_filters_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "all-filters-pill-button")]')))
                all_filters_btn.click()
                print("✅ Opened 'All filters' popup.")
                time.sleep(2)

                # Filters inside the popup:
                # 1. Past 24 hours
                try:
                    past_24 = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[contains(.,"Past 24 hours")]')))
                    past_24.click()
                except: print("⚠️ 'Past 24 hours' not found.")

                # 2. Experience level
                for level in ["Internship", "Entry level"]:
                    try:
                        label = wait.until(EC.element_to_be_clickable((By.XPATH, f'//label[contains(.,"{level}")]')))
                        label.click()
                    except: print(f"⚠️ '{level}' not found.")

                # 3. Remote only if not Budapest
                if "Budapest" not in location:
                    try:
                        remote = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[contains(.,"Remote")]')))
                        remote.click()
                    except: print("⚠️ 'Remote' not found.")

                # 4. Easy Apply
                try:
                    easy_apply = wait.until(EC.element_to_be_clickable((By.XPATH, '//label[contains(.,"Easy Apply")]')))
                    easy_apply.click()
                except: print("⚠️ 'Easy Apply' not found.")

                # Show results
                show_results_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button//span[text()="Show results"]')))
                show_results_btn.click()
                print("✅ Filters applied & results shown.")
                time.sleep(5)

            except Exception as e:
                print(f"❌ Error during filtering: {e}")