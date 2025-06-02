#main.py
from src.Login.login import driver
from src.Feed.feed import simulate_human_behavior

# Driver automated on the feed
simulate_human_behavior(driver)

#Progress
print("Now it's ready to move to Job application section")