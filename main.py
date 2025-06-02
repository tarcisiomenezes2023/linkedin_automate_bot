#main.py
from src.Login.login import driver
from src.Feed.feed import simulate_human_behavior
from src.Filter.filter import filter_jobs

# Driver automated on the feed
simulate_human_behavior(driver)

# Job Application
filter_jobs(driver)