import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config.settings import Config

def setup_logger():
    logger = logging.getLogger('linkedin_bot')
    logger.setLevel(logging.INFO)
    
    # Create logs directory if not exists
    Config.DATA_DIR.mkdir(exist_ok=True)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(levelname)s - %(message)s'
    ))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = setup_logger()