import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / 'config' / 'credentials.env')

class Config:
    # Browser Settings
    HEADLESS = False
    USER_AGENT_ROTATION = True
    PROXY_LIST = [
        '103.156.19.229:3128',
        '45.70.236.123:999',
        '200.105.215.18:33630'
    ]
    
    # LinkedIn Credentials
    LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
    LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')
    
    # Search Parameters
    SEARCH_KEYWORDS = "python OR excel OR frontend"
    LOCATION = "Budapest"
    EXPERIENCE_LEVELS = ["Internship", "Entry level"]
    
    # Behavior Settings
    MAX_DAILY_APPLICATIONS = (5, 15)  # Random range
    INTER_JOB_DELAYS = (10, 30)      # Seconds between jobs
    WORKING_HOURS = ('09:00', '17:00')
    
    # Paths
    DATA_DIR = BASE_DIR / 'data'
    LOG_FILE = DATA_DIR / 'bot.log'
    SCREENSHOT_DIR = DATA_DIR / 'screenshots'
    PROFILES_DIR = DATA_DIR / 'profiles'
    
    # Humanizer Settings
    TYPO_CHANCE = 0.03
    MOUSE_MOVE_POINTS = 30
    MIN_DELAY = 0.05
    MAX_DELAY = 0.3