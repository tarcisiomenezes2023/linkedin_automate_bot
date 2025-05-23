# Browser Setup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import random
import time

def get_random_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
    user_agent_rotator = UserAgent(software_names=software_names, 
                                  operating_systems=operating_systems, 
                                  limit=100)
    return user_agent_rotator.get_random_user_agent()

def create_browser_instance(headless=False):
    options = Options()
    
    # Randomize browser fingerprint
    options.add_argument(f'user-agent={get_random_user_agent()}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Random window size
    width = random.randint(1200, 1400)
    height = random.randint(800, 1000)
    options.add_argument(f"window-size={width},{height}")
    
    # Configure proxy if needed (rotate proxies to avoid detection)
    
    driver = uc.Chrome(options=options, headless=headless)
    
    # Further human-like configuration
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver