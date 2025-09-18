"""Session management for Tempo.co scraper."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .logging import logger

def create_session() -> requests.Session:
    """
    Create a requests session with retry strategy.
    
    Returns:
        Configured requests session
    """
    session = requests.Session()
    
    # Define retry strategy
    # This will retry on 429, 500, 502, 503, 504 status codes
    # with exponential backoff
    retry_strategy = Retry(
        total=3,  # Total number of retries
        status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
        backoff_factor=1,  # Backoff factor for exponential backoff
        raise_on_status=False  # Don't raise exception on status, let the caller handle it
    )
    
    # Create adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Mount adapter for both HTTP and HTTPS
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session