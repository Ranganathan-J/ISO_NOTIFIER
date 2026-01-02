"""
Web search scraper using DuckDuckGo to find compliance prerequisites.
"""
from ddgs import DDGS
import logging
import time
import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger("ComplianceAssistant.Scraper")

def search_prerequisites(title, description, max_results=8):
    """
    Search DuckDuckGo for compliance prerequisites.
    
    Args:
        title: Compliance item title
        description: Compliance item description
        max_results: Maximum number of search results
    
    Returns:
        List of dictionaries with search results
    """
    try:
        # Search for official documentation, prerequisites, AND validity/expiry rules
        main_query = f"{title} official certification requirements prerequisites validity period renewal cycle expiry site:iso.org OR site:bsigroup.com OR site:tuv.com OR site:intertek.com"
        backup_query = f"{title} {description[:100]} certificate validity renewal period requirements"
        
        logger.info(f"Searching DuckDuckGo: {main_query}")
        
        all_results = []
        with DDGS() as ddgs:
            # Try official search first
            official_results = list(ddgs.text(main_query, max_results=max_results))
            all_results.extend(official_results)
            
            # If few results, supplement with the general query
            if len(all_results) < 4:
                logger.info("Supplementing with general search results")
                general_results = list(ddgs.text(backup_query, max_results=max_results - len(all_results)))
                all_results.extend(general_results)
        
        # Enrich results with page content
        enriched_results = []
        for idx, result in enumerate(all_results[:max_results]):
            try:
                # Fetch page content
                content = fetch_page_content(result['href'])
                
                # Use page content if found, otherwise fallback to snippet
                enriched_results.append({
                    'title': result['title'],
                    'url': result['href'],
                    'snippet': result['body'],
                    'content': content if content else result['body']
                })
                
                # Rate limiting to avoid blocking
                time.sleep(1)
            
            except Exception as e:
                logger.warning(f"Could not fetch content from {result['href']}: {str(e)}")
                enriched_results.append({
                    'title': result['title'],
                    'url': result['href'],
                    'snippet': result['body'],
                    'content': result.get('body', '')
                })
        
        # Save raw data for auditing
        save_raw_data(title, enriched_results)
        
        logger.info(f"Found {len(enriched_results)} search results")
        return enriched_results
    
    except Exception as e:
        logger.error(f"Error during web search: {str(e)}")
        return []

def fetch_page_content(url, timeout=10):
    """
    Fetch and parse HTML content from a URL.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
    
    Returns:
        Extracted text content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit to first 5000 characters
        return text[:5000]
    
    except Exception as e:
        logger.warning(f"Error fetching {url}: {str(e)}")
        return None

def save_raw_data(title, results):
    """
    Save raw search results to JSON file for auditing.
    
    Args:
        title: Compliance item title
        results: Search results to save
    """
    try:
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from title
        filename = "".join(c if c.isalnum() else "_" for c in title)[:50]
        filepath = raw_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved raw data to {filepath}")
    
    except Exception as e:
        logger.error(f"Error saving raw data: {str(e)}")
