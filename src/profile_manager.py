import os
import random
import json
from datetime import datetime
from humanizer import Humanizer

class ProfileManager:
    def __init__(self):
        self.profiles_dir = "../data/profiles/"
        self.load_profiles()
        
    def load_profiles(self):
        """Load all available profiles"""
        self.resumes = []
        self.cover_letters = []
        self.profile_data = {}
        
        # Load resume files
        for file in os.listdir(os.path.join(self.profiles_dir, "resumes")):
            if file.endswith(".pdf"):
                self.resumes.append(file)
        
        # Load cover letters
        for file in os.listdir(os.path.join(self.profiles_dir, "cover_letters")):
            if file.endswith(".pdf") or file.endswith(".docx"):
                self.cover_letters.append(file)
        
        # Load profile data
        with open(os.path.join(self.profiles_dir, "profiles.json"), 'r') as f:
            self.profile_data = json.load(f)
    
    def get_random_profile(self):
        """Select a random profile variation"""
        profile = random.choice(self.profile_data["profiles"])
        
        # Randomize some details
        if random.random() > 0.7:  # 30% chance to slightly modify
            profile["phone"] = self.randomize_phone(profile["phone"])
            profile["address"] = random.choice(self.profile_data["addresses"])
        
        return {
            "resume": os.path.join(self.profiles_dir, "resumes", random.choice(self.resumes)),
            "cover_letter": os.path.join(self.profiles_dir, "cover_letters", random.choice(self.cover_letters)),
            "profile": profile
        }
    
    def randomize_phone(self, phone):
        """Slightly modify phone number"""
        digits = list(phone.replace("-", "").replace(" ", ""))
        if len(digits) >= 10:
            # Change one random digit
            idx = random.randint(0, len(digits)-1)
            digits[idx] = str(random.randint(0, 9))
        return "".join(digits)
    
    def record_application(self, job_info, profile_used):
        """Record which profile was used for which application"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "job": job_info,
            "profile": profile_used
        }
        
        with open(os.path.join(self.profiles_dir, "application_history.json"), 'a') as f:
            f.write(json.dumps(record) + "\n")