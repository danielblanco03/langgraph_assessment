import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import ClassVar, Dict

load_dotenv()

class Config(BaseSettings):
    """
    Configuration for the Stock Analysis Agent.
    """
    
    # Request timeout settings
    REQUEST_TIMEOUT: int = 10  # seconds
    MAX_RETRIES: int = 3

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }

# Instantiate global config object
config = Config()