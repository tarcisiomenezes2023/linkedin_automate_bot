from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.humanizer import Humanizer
from src.utils.logger import logger
from config.settings import Config
import time
import random

class JobFilters:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        
    def search_jobs(self, keywords=None, location=None, experience_levels=None):
        """Search for jobs with given filters"""
        keywords = keywords or Config.SEARCH_KEYWORDS
        location = location or Config.LOCATION
        experience_levels = experience_levels or Config.EXPERIENCE_LEVELS
        
        try:
            logger.info(f"Searching jobs: {keywords} in {location}")
            self.driver.get("https://www.linkedin.com/jobs")
            self.humanizer.random_delay(3, 5)
            
            # Search keywords
            search_keywords = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]")
                )
            )
            self.humanizer.human_type(search_keywords, keywords)
            self.humanizer.random_delay(1, 2)
            
            # Search location
            search_location = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[contains(@id, 'jobs-search-box-location')]")
                )
            )
            search_location.clear()
            self.humanizer.random_delay(1, 2)
            self.humanizer.human_type(search_location, location)
            self.humanizer.random_delay(1, 2)
            search_location.send_keys(Keys.RETURN)
            
            # Apply filters
            self.apply_experience_filter(experience_levels)
            
            return self.get_job_listings()
            
        except TimeoutException as e:
            logger.error("Job search page elements not found")
            raise
        except Exception as e:
            logger.error(f"Job search failed: {str(e)}")
            raise
            
    def apply_experience_filter(self, experience_levels):
        """Apply experience level filters"""
        try:
            if not experience_levels:
                return
                
            logger.info(f"Applying experience filters: {experience_levels}")
            exp_filter = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Experience level filter')]")
                )
            )
            self.humanizer.human_click(exp_filter)
            self.humanizer.random_delay(1, 2)
            
            for level in experience_levels:
                checkbox = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//label[contains(@for, 'experience-{level.lower().replace(' ', '-')}')]")
                    )
                )
                self.humanizer.human_click(checkbox)
                self.humanizer.random_delay(0.5, 1)
            
            apply_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Apply current filters')]")
                )
            )
            self.humanizer.human_click(apply_button)
            self.humanizer.random_delay(2, 4)
            
        except Exception as e:
            logger.warning(f"Could not apply experience filters: {str(e)}")
            
    def get_job_listings(self, max_scrolls=3):
        """Extract job listings from search results"""
        try:
            logger.info("Extracting job listings")
            self.humanizer.random_delay(3, 5)
            
            # Scroll to load more jobs
            for _ in range(max_scrolls):
                self.humanizer.random_scroll()
                self.humanizer.random_delay(1, 2)
            
            job_cards = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, 'jobs-search-results-list')]//li")
                )
            )
            
            jobs = []
            for card in job_cards:
                try:
                    title_elem = card.find_element(
                        By.XPATH, ".//a[contains(@class, 'job-card-list__title')]"
                    )
                    company_elem = card.find_element(
                        By.XPATH, ".//span[contains(@class, 'job-card-container__primary-description')]"
                    )
                    location_elem = card.find_element(
                        By.XPATH, ".//li[contains(@class, 'job-card-container__metadata-item')]"
                    )
                    link = title_elem.get_attribute('href')
                    
                    jobs.append({
                        'title': title_elem.text.strip(),
                        'company': company_elem.text.strip(),
                        'location': location_elem.text.strip(),
                        'link': link,
                        'element': card
                    })
                except NoSuchElementException:
                    continue
                    
            logger.info(f"Found {len(jobs)} matching jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"Failed to extract job listings: {str(e)}")
            raise