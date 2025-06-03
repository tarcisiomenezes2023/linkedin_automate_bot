#main.py
from src.Login.login import driver
from src.Feed.feed import simulate_human_behavior
from src.Filter.remote_filter import Remote_filter_jobs

# Driver automated on the feed
simulate_human_behavior(driver)

# Job Application
Remote_filter_jobs(driver)