"""URL building utilities for Tempo.co scraper."""

from datetime import datetime, timedelta
from typing import Optional
from ..core.selectors import BASE_URL

def build_index_url(
    page: int = 1,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    rubric: Optional[str] = None
) -> str:
    """
    Build index URL with page and optional date/rubric parameters.
    
    Note: Rubric and date filters are mutually exclusive. If both are provided, rubric takes precedence.
    
    Args:
        page: Page number
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        rubric: Rubric slug
        
    Returns:
        Constructed URL
    """
    url = f"{BASE_URL}?page={page}"
    
    # Add rubric parameter if provided (takes precedence over date filters)
    if rubric:
        url += f"&category=rubrik&rubric_slug={rubric}"
    # Add date parameters if provided (only if rubric is not provided)
    elif start_date and end_date:
        url += f"&category=date&start_date={start_date}&end_date={end_date}"
    elif start_date:  # Only start_date provided, create 1-day difference
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)
        end_date = end_dt.strftime("%Y-%m-%d")
        url += f"&category=date&start_date={start_date}&end_date={end_date}"
    elif end_date:  # Only end_date provided, create 1-day difference
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_dt = end_dt - timedelta(days=1)
        start_date = start_dt.strftime("%Y-%m-%d")
        url += f"&category=date&start_date={start_date}&end_date={end_date}"
    
    return url