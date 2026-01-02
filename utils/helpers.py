"""
General helper utilities for the Compliance Assistant.
"""
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("ComplianceAssistant.Helpers")

def format_date(date_obj, format_str='%Y-%m-%d'):
    """
    Format datetime object to string.
    
    Args:
        date_obj: datetime object
        format_str: Output format string
    
    Returns:
        Formatted date string
    """
    if not date_obj:
        return "N/A"
    
    if isinstance(date_obj, str):
        return date_obj
    
    return date_obj.strftime(format_str)

def is_overdue(due_date):
    """
    Check if a compliance item is overdue.
    
    Args:
        due_date: Due date (datetime or string)
    
    Returns:
        True if overdue, False otherwise
    """
    if isinstance(due_date, str):
        from utils.data_cleaning import parse_date
        due_date = parse_date(due_date)
    
    if not due_date:
        return False
    
    return datetime.now() > due_date

def get_urgency_level(due_date):
    """
    Determine urgency level based on due date.
    
    Args:
        due_date: Due date (datetime or string)
    
    Returns:
        Urgency level: 'critical', 'high', 'medium', 'low'
    """
    if isinstance(due_date, str):
        from utils.data_cleaning import parse_date
        due_date = parse_date(due_date)
    
    if not due_date:
        return 'low'
    
    days_until_due = (due_date - datetime.now()).days
    
    if days_until_due < 0:
        return 'critical'  # Overdue
    elif days_until_due <= 3:
        return 'critical'
    elif days_until_due <= 7:
        return 'high'
    elif days_until_due <= 14:
        return 'medium'
    else:
        return 'low'

def truncate_text(text, max_length=100):
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text with ellipsis if needed
    """
    if not text:
        return ""
    
    text = str(text)
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."
