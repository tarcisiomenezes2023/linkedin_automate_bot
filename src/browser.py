# Browser Setup
def create_browser_instance(headless=False):
    options = Options()
    
    # Randomize multiple fingerprint aspects
    user_agent = get_random_user_agent()
    options.add_argument(f'user-agent={user_agent}')
    
    # Randomize screen resolution
    width = random.choice([1366, 1440, 1536, 1600, 1920])
    height = random.choice([768, 900, 960, 1080, 1200])
    options.add_argument(f"--window-size={width},{height}")
    
    # Randomize other properties
    options.add_argument(f"--lang={random.choice(['en-US', 'en-GB', 'en-CA'])}")
    options.add_argument(f"--timezone={random.choice(['America/New_York', 'Europe/London', 'Asia/Singapore'])}")
    
    # Configure proxy rotation (example using free proxies)
    proxy_list = [
        '103.156.19.229:3128',
        '45.70.236.123:999',
        '200.105.215.18:33630'
    ]
    proxy = random.choice(proxy_list)
    options.add_argument(f'--proxy-server={proxy}')
    
    # Disable automation flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = uc.Chrome(options=options, headless=headless)
    
    # Override navigator properties
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3]
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });
        """
    })
    
    return driver