"""Session management module for Tempo.co scraper."""

import requests
from .selectors import HEADERS
from .logging import logger

def create_session() -> requests.Session:
    """
    Create a requests session.
    
    Returns:
        Configured requests session
    """
    session = requests.Session()
    
    # Set default headers
    session.headers.update(HEADERS)
    
    return session