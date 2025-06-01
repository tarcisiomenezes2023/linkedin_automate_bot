from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, InvalidElementStateException
from src.humanizer import Humanizer
from src.utils.logger import logger
from src.utils.exceptions import LinkedInAuthError
from config.settings import Config
import time

class LinkedIn:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        
    def login(self):
        """Login to LinkedIn with human-like behavior"""
        try:
            logger.info("Starting LinkedIn login process")
            self.driver.get("https://www.linkedin.com/login")
            self.humanizer.random_delay(2, 4)
            
            # Fill email
            email = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            self.humanizer.human_type(email, Config.LINKEDIN_EMAIL)
            
            # Fill password
            password = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            self.humanizer.human_type(password, Config.LINKEDIN_PASSWORD)
            
            # Click login
            self.humanizer.random_delay(1, 3)
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            self.humanizer.human_click(login_button)
            
            # Verify login
            self.humanizer.random_delay(3, 5)
            if not self.is_logged_in():
                raise LinkedInAuthError("Login verification failed")
                
            logger.info("Successfully logged in to LinkedIn")
            return True
            
        except TimeoutException as e:
            error_msg = "Login page elements not found"
            logger.error(error_msg)
            raise LinkedInAuthError(error_msg) from e
            
        except InvalidElementStateException as e:
            error_msg = "Login form in invalid state"
            logger.error(error_msg)
            raise LinkedInAuthError(error_msg) from e
            
        except Exception as e:
            error_msg = f"Unexpected login error: {str(e)}"
            logger.error(error_msg)
            raise LinkedInAuthError(error_msg) from e
            
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.ID, "global-nav-typeahead"))
            )
            return True
        except:
            return False
            
    def take_screenshot(self, name):
        """Save screenshot to data/screenshots"""
        Config.SCREENSHOT_DIR.mkdir(exist_ok=True)
        path = Config.SCREENSHOT_DIR / f"{name}_{int(time.time())}.png"
        self.driver.save_screenshot(str(path))
        return path