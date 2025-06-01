import time
from datetime import datetime
from typing import Dict, Any

class PerformanceTracker:
    def __init__(self):
        self.start_time = time.time()
        self.jobs_processed = 0
        self.errors = 0
        self.start_date = datetime.now().strftime('%Y-%m-%d')
        
    def record_success(self):
        self.jobs_processed += 1
        
    def record_error(self):
        self.errors += 1
        
    def get_metrics(self) -> Dict[str, Any]:
        duration = time.time() - self.start_time
        total_attempts = self.jobs_processed + self.errors
        return {
            'date': self.start_date,
            'duration_seconds': round(duration, 2),
            'jobs_processed': self.jobs_processed,
            'errors': self.errors,
            'success_rate': round(self.jobs_processed / max(1, total_attempts) * 100, 2),
            'jobs_per_hour': round(self.jobs_processed / (duration / 3600), 2)
        }