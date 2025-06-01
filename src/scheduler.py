import schedule
import time
import random
from datetime import datetime, timedelta
import logging
from main import main  # Import your main function

class JobScheduler:
    def __init__(self):
        self.logger = self.setup_logger()
        self.working_hours = {
            'start': datetime.strptime('09:00', '%H:%M').time(),
            'end': datetime.strptime('17:00', '%H:%M').time()
        }
        self.max_daily_applications = random.randint(5, 15)
        self.current_applications = 0
        
    def setup_logger(self):
        logger = logging.getLogger('linkedin_bot')
        logger.setLevel(logging.INFO)
        
        # Create file handler
        fh = logging.FileHandler('../data/bot.log')
        fh.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        logger.addHandler(fh)
        return logger
    
    def should_run(self):
        """Check if bot should run based on time and daily limits"""
        now = datetime.now().time()
        weekday = datetime.now().weekday()
        
        # Don't run on weekends
        if weekday >= 5:  # 5 = Saturday, 6 = Sunday
            self.logger.info("It's weekend - not running")
            return False
            
        # Check working hours
        if not (self.working_hours['start'] <= now <= self.working_hours['end']):
            self.logger.info("Outside working hours - not running")
            return False
            
        # Check daily application limit
        if self.current_applications >= self.max_daily_applications:
            self.logger.info("Reached daily application limit - not running")
            return False
            
        return True
    
    def random_job(self):
        """Main job with random delays and checks"""
        if self.should_run():
            try:
                self.logger.info("Starting job application run")
                main()
                self.current_applications += 1
                self.logger.info(f"Completed run. Total today: {self.current_applications}")
            except Exception as e:
                self.logger.error(f"Error in job run: {str(e)}")
        
        # Randomize next run time (between 30-120 minutes)
        next_run = random.randint(30, 120)
        self.logger.info(f"Next run in {next_run} minutes")
        return next_run
    
    def start(self):
        """Start the scheduling system"""
        self.logger.info("Starting LinkedIn Bot Scheduler")
        
        # Initial random delay (1-10 minutes)
        time.sleep(random.randint(60, 600))
        
        # Continuous scheduling
        while True:
            next_run = self.random_job()
            time.sleep(next_run * 60)
            
            # Reset daily counter if new day
            now = datetime.now()
            if now.hour == 0 and now.minute < 5:
                self.current_applications = 0
                self.max_daily_applications = random.randint(5, 15)
                self.logger.info("Reset daily application counter")