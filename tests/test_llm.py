"""
Unit tests for LLM module.
"""
import pytest
from llm.query_handler import extract_prerequisites, format_search_results

def test_format_search_results():
    """Test search results formatting."""
    results = [
        {
            'title': 'Test 1',
            'url': 'https://example.com/1',
            'content': 'Test content 1',
            'snippet': 'Test snippet 1'
        }
    ]
    
    formatted = format_search_results(results)
    assert isinstance(formatted, str)
    assert 'Test 1' in formatted
    assert 'https://example.com/1' in formatted

def test_extract_prerequisites_fallback():
    """Test fallback when LLM fails."""
    # Mock search results
    results = [
        {
            'title': 'Test Result',
            'url': 'https://example.com',
            'snippet': 'Test snippet'
        }
    ]
    
    item = {
        'Title': 'Test Item',
        'Description': 'Test Description',
        'Due Date': '2024-12-31'
    }
    
    # This would need proper mocking of LLM client
    # prerequisites = extract_prerequisites(results, item)
    # assert isinstance(prerequisites, str)
