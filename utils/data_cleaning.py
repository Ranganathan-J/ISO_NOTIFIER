"""
Data cleaning and normalization utilities.
"""
import re
from datetime import datetime
import logging

logger = logging.getLogger("ComplianceAssistant.DataCleaning")

def clean_text(text):
    """
    Clean and normalize text data.
    
    Args:
        text: Raw text to clean
    
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Convert to string
    text = str(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Trim
    text = text.strip()
    
    return text

def extract_email(text):
    """
    Extract email address from text.
    
    Args:
        text: Text containing email
    
    Returns:
        Email address or None
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None

def validate_email(email):
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
    
    Returns:
        True if valid, False otherwise
    """
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return re.match(email_pattern, str(email)) is not None

def parse_date(date_str):
    """
    Parse date string to datetime object.
    
    Args:
        date_str: Date string in various formats
    
    Returns:
        datetime object or None
    """
    if isinstance(date_str, datetime):
        return date_str
    
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%B %d, %Y',
        '%d %B %Y'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str).strip(), fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date: {date_str}")
    return None

def normalize_title(title):
    """
    Normalize compliance item title for comparison.
    
    Args:
        title: Raw title
    
    Returns:
        Normalized title
    """
    if not title:
        return ""
    
    # Convert to lowercase
    title = str(title).lower()
    
    # Remove extra whitespace
    title = re.sub(r'\s+', ' ', title)
    
    # Remove special characters
    title = re.sub(r'[^\w\s]', '', title)
    
    return title.strip()
