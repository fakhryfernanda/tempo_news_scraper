"""Configuration module for Tempo.co scraper."""

from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)