"""
Unit tests for utilities module.
"""
import pytest
from utils.data_cleaning import clean_text, validate_email, parse_date, normalize_title
from utils.helpers import format_date, get_urgency_level, truncate_text
from datetime import datetime

def test_clean_text():
    """Test text cleaning."""
    assert clean_text("  Hello   World  ") == "Hello World"
    assert clean_text("Test!@#$%") == "Test"
    assert clean_text(None) == ""

def test_validate_email():
    """Test email validation."""
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    assert validate_email("test@domain") == False

def test_parse_date():
    """Test date parsing."""
    date = parse_date("2024-12-31")
    assert isinstance(date, datetime)
    assert date.year == 2024
    assert date.month == 12
    assert date.day == 31

def test_normalize_title():
    """Test title normalization."""
    assert normalize_title("Test Title!") == "test title"
    assert normalize_title("HELLO WORLD") == "hello world"

def test_format_date():
    """Test date formatting."""
    date = datetime(2024, 12, 31)
    assert format_date(date) == "2024-12-31"
    assert format_date(None) == "N/A"

def test_get_urgency_level():
    """Test urgency level calculation."""
    from datetime import timedelta
    
    # Future dates
    tomorrow = datetime.now() + timedelta(days=1)
    assert get_urgency_level(tomorrow) == 'critical'
    
    next_week = datetime.now() + timedelta(days=5)
    assert get_urgency_level(next_week) == 'high'

def test_truncate_text():
    """Test text truncation."""
    long_text = "a" * 200
    truncated = truncate_text(long_text, 100)
    assert len(truncated) == 100
    assert truncated.endswith("...")
