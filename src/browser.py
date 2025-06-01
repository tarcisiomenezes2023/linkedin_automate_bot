import random
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from src.utils.logger import logger
from src.utils.exceptions import BrowserError
from config.settings import Config

def get_random_user_agent():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(
        software_names=software_names,
        operating_systems=operating_systems,
        limit=100
    )
    return user_agent_rotator.get_random_user_agent()

def create_browser_instance(headless=None):
    """Create and configure a browser instance with human-like settings"""
    try:
        headless = Config.HEADLESS if headless is None else headless
        options = Options()
        
        # Randomize fingerprint
        if Config.USER_AGENT_ROTATION:
            options.add_argument(f'user-agent={get_random_user_agent()}')
        
        # Randomize viewport
        width, height = random.choice([
            (1366, 768), (1440, 900), 
            (1536, 960), (1920, 1080)
        ])
        options.add_argument(f"--window-size={width},{height}")
        
        # Language and timezone
        options.add_argument(f"--lang={random.choice(['en-US', 'en-GB', 'en-CA'])}")
        options.add_argument(f"--timezone={random.choice(['America/New_York', 'Europe/London', 'Asia/Singapore'])}")
        
        # Proxy configuration
        if Config.PROXY_LIST:
            proxy = random.choice(Config.PROXY_LIST)
            options.add_argument(f'--proxy-server={proxy}')
        
        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        driver = uc.Chrome(
            options=options,
            headless=headless,
            version_main=114  # Specify Chrome version
        )
        
        # Override navigator properties
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            """
        })
        
        logger.info("Browser instance created successfully")
        return driver
        
    except Exception as e:
        logger.error(f"Browser initialization failed: {str(e)}")
        raise BrowserError(f"Could not create browser instance: {str(e)}")