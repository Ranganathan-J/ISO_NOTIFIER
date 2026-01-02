"""
Handle LLM queries for prerequisite extraction and enrichment.
"""
from llm.llm_client import get_llm_client, create_prerequisite_prompt
import logging

logger = logging.getLogger("ComplianceAssistant.QueryHandler")

def extract_prerequisites(search_results, item):
    """
    Use LLM to extract prerequisites from search results.
    
    Args:
        search_results: List of search result dictionaries
        item: Compliance item dictionary
    
    Returns:
        Extracted prerequisites as formatted text
    """
    try:
        # Initialize LLM
        llm = get_llm_client()
        prompt_template = create_prerequisite_prompt()
        
        # Format search results for prompt
        formatted_results = format_search_results(search_results)
        
        # Create prompt
        prompt = prompt_template.format(
            title=item['Title'],
            description=item['Description'],
            application_date=item.get('Application Date', 'Not specified'),
            search_results=formatted_results
        )
        
        # Invoke LLM
        logger.info("Invoking LLM for prerequisite and expiry extraction")
        response = llm.invoke(prompt)
        
        # Extract content
        content = response.content
        logger.info("Successfully received LLM response")
        
        # Parse the structured response
        parsed_result = {
            'prerequisites': content,
            'due_date': None,
            'validity': None
        }
        
        import re
        due_date_match = re.search(r"\[DUE_DATE\]:\s*(\d{4}-\d{2}-\d{2})", content)
        validity_match = re.search(r"\[VALIDITY_PERIOD\]:\s*(.*)", content)
        
        if due_date_match:
            parsed_result['due_date'] = due_date_match.group(1).strip()
        if validity_match:
            parsed_result['validity'] = validity_match.group(1).strip()
            
        # Clean up prerequisites text by removing the tags
        clean_prereqs = re.sub(r"\[DUE_DATE\]:.*", "", content)
        clean_prereqs = re.sub(r"\[VALIDITY_PERIOD\]:.*", "", clean_prereqs).strip()
        parsed_result['prerequisites'] = clean_prereqs
        
        return parsed_result
    
    except Exception as e:
        logger.error(f"Error extracting prerequisites: {str(e)}")
        # Fallback: return formatted search snippets in the expected dict format
        return {
            'prerequisites': format_fallback_prerequisites(search_results, item),
            'due_date': None,
            'validity': None
        }

def format_search_results(results):
    """
    Format search results for LLM prompt.
    
    Args:
        results: List of search result dictionaries
    
    Returns:
        Formatted string of search results
    """
    formatted = []
    for idx, result in enumerate(results, 1):
        content = result.get('content') or result.get('snippet', '')
        formatted.append(f"Source {idx}: {result['title']}\nURL: {result['url']}\n{content[:1000]}\n")
    
    return "\n---\n".join(formatted)

def format_fallback_prerequisites(results, item):
    """
    Create fallback prerequisites if LLM fails.
    
    Args:
        results: Search results
        item: Compliance item
    
    Returns:
        Formatted prerequisites text
    """
    prereqs = f"Prerequisites for {item['Title']}:\n\n"
    prereqs += "Based on web search, please review the following sources:\n\n"
    
    for idx, result in enumerate(results, 1):
        prereqs += f"{idx}. {result['title']}\n   {result['url']}\n"
        prereqs += f"   {result.get('snippet', '')[:200]}...\n\n"
    
    return prereqs
