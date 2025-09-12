"""Date and time parsing utilities for Tempo.co scraper."""

from typing import Dict

def parse_publication_datetime(pub_date_str: str) -> Dict[str, str]:
    """
    Parse publication date string and separate into date and time components.
    
    Args:
        pub_date_str: Publication date string in format "12 September 2025 | 15.22 WIB"
        
    Returns:
        Dictionary with date, time, and timezone components
    """
    if not pub_date_str:
        return {"date": "", "time": "", "timezone": ""}
    
    try:
        # Split by the pipe separator
        parts = pub_date_str.split(" | ")
        if len(parts) != 2:
            return {"date": "", "time": "", "timezone": ""}
        
        date_part = parts[0].strip()
        time_part = parts[1].strip()
        
        # Parse date part (e.g., "12 September 2025")
        months = {
            "January": "01", "February": "02", "March": "03", "April": "04",
            "May": "05", "June": "06", "July": "07", "August": "08",
            "September": "09", "October": "10", "November": "11", "December": "12"
        }
        
        date_components = date_part.split()
        if len(date_components) == 3:
            day = date_components[0].zfill(2)
            month_name = date_components[1]
            year = date_components[2]
            
            month = months.get(month_name, "01")
            formatted_date = f"{year}-{month}-{day}"
        else:
            formatted_date = ""
        
        # Parse time part (e.g., "15.22 WIB")
        time_components = time_part.split()
        if len(time_components) >= 1:
            time_str = time_components[0]
            # Convert dot to colon (15.22 -> 15:22)
            time_parts = time_str.split('.')
            if len(time_parts) == 2:
                hour = time_parts[0].zfill(2)
                minute = time_parts[1].zfill(2)
                formatted_time = f"{hour}:{minute}:00"
            else:
                formatted_time = ""
            timezone = time_components[1] if len(time_components) > 1 else ""
        else:
            formatted_time = ""
            timezone = ""
        
        return {
            "date": formatted_date,
            "time": formatted_time,
            "timezone": timezone
        }
    except Exception:
        return {"date": "", "time": "", "timezone": ""}