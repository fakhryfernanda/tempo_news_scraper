"""Validation utilities for Tempo.co scraper."""

from datetime import datetime, timedelta
from typing import Tuple, Optional

def validate_date_format(date_str: str, date_type: str) -> bool:
    """
    Validate that the date string is in YYYY-MM-DD format.
    
    Args:
        date_str: Date string to validate
        date_type: Type of date (for error messages)
        
    Returns:
        True if valid, False otherwise
    """
    if date_str:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            print(f"Error: {date_type} must be in YYYY-MM-DD format")
            return False
    return True

def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    Validate that start_date is not later than end_date.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        True if valid, False otherwise
    """
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start_dt > end_dt:
            print("Error: start-date cannot be later than end-date")
            return False
    return True

def validate_page_range(start_page: int, end_page: int) -> bool:
    """
    Validate that the page range is not too large.
    
    Args:
        start_page: Starting page number
        end_page: Ending page number
        
    Returns:
        True if valid, False otherwise
    """
    if end_page - start_page > 50:
        print("Warning: You're trying to scrape more than 50 pages.")
        print("Please limit your scraping to be respectful to the server.")
        return False
    return True

def process_dates(start_date: Optional[str], end_date: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Process dates, creating 1-day difference if only one date is provided.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Tuple of (start_date, end_date)
    """
    # If only start_date is provided, create 1-day difference
    if start_date and not end_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = start_dt + timedelta(days=1)
        end_date = end_dt.strftime('%Y-%m-%d')
    # If only end_date is provided, create 1-day difference
    elif end_date and not start_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        start_dt = end_dt - timedelta(days=1)
        start_date = start_dt.strftime('%Y-%m-%d')
    
    return start_date, end_date