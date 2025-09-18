"""Session management module for Tempo.co scraper."""

import requests
from .selectors import HEADERS
from .logging import logger

def create_session(use_auth: bool = False) -> requests.Session:
    """
    Create a requests session.
    
    Args:
        use_auth: Whether to use authentication (ignored, always uses anonymous session)
        
    Returns:
        Configured requests session
    """
    session = requests.Session()
    
    # Set default headers
    session.headers.update(HEADERS)
    
    logger.info("Using anonymous session")
    
    return session