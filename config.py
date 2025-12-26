# config.py
import os
from dotenv import load_dotenv
from utils.logger import log

# Load environment variables from the .env file
load_dotenv()

class Config:
    """Central configuration management."""
    
    # API Keys
    LEAKCHECK_API_KEY = os.getenv("LEAKCHECK_API_KEY")
    
    
    # Settings
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./reports")
    TIMEOUT = int(os.getenv("TIMEOUT", 10))

    @staticmethod
    def validate():
        """Checks if critical keys are missing and warns the user."""
        if not Config.LEAKCHECK_API_KEY:
            log.warning("LeakCheck API key is missing. Breach lookups may fail.")