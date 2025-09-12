"""Session management module for Tempo.co scraper."""

import os
import requests
from typing import Optional
from .selectors import HEADERS
from .logging import logger

def get_session_id() -> Optional[str]:
    """
    Get REMP_SESSION_ID from environment variables.
    
    Returns:
        REMP_SESSION_ID if available, None otherwise
    """
    return os.getenv('REMP_SESSION_ID')

def create_session(use_auth: bool = False) -> requests.Session:
    """
    Create a requests session with optional authentication.
    
    Args:
        use_auth: Whether to use authentication
        
    Returns:
        Configured requests session
    """
    session = requests.Session()
    
    # Set default headers
    session.headers.update(HEADERS)
    
    if use_auth:
        session_id = get_session_id()
        if session_id:
            session.cookies.set('remp_session_id', session_id)
            logger.info("Using authenticated session")
        else:
            logger.warning("No REMP_SESSION_ID found, using anonymous session")
    else:
        logger.info("Using anonymous session")
    
    return session