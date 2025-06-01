class LinkedInBotError(Exception):
    """Base exception for all bot-related errors"""
    pass

class BrowserError(LinkedInBotError):
    """Browser-related exceptions"""
    pass

class LinkedInAuthError(LinkedInBotError):
    """LinkedIn authentication failures"""
    pass

class JobApplicationError(LinkedInBotError):
    """Job application failures"""
    pass

class RateLimitExceeded(LinkedInBotError):
    """When LinkedIn rate limits are hit"""
    pass