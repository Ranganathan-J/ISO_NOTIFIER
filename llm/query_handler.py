from llm.llm_client import get_llm_client, create_prerequisite_prompt
from utils.due_date_manager import DueDateManager
import logging

logger = logging.getLogger("ComplianceAssistant.QueryHandler")

# Initialize manager
due_date_manager = DueDateManager()

def extract_prerequisites(search_results, item):
    """
    Use LLM to extract prerequisites and determine due date using DueDateManager.
    
    Args:
        search_results: List of search result dictionaries
        item: Compliance item dictionary
    
    Returns:
        Dictionary with prerequisites, due_date, and metadata
    """
    try:
        # Step 1: Calculate high-confidence due date using DueDateManager
        logger.info("Calculating intelligent due date...")
        dd_result = due_date_manager.calculate_due_date(item, search_results)
        
        # Step 2: Extract prerequisites using the specialized prompt
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
        
        # Invoke LLM for prerequisites
        logger.info("Invoking LLM for prerequisite extraction")
        response = llm.invoke(prompt)
        
        # Extract content
        content = response.content
        logger.info("Successfully received LLM response")
        
        # Merge results
        parsed_result = {
            'prerequisites': content,
            'due_date': dd_result.due_date.strftime('%Y-%m-%d'),
            'validity': dd_result.validity_period,
            'confidence': dd_result.confidence,
            'calculation_method': dd_result.method.value,
            'calculation_notes': dd_result.calculation_notes,
            'warning': dd_result.warning
        }
        
        # Clean up prerequisites text (remove any artifact tags if they still exist)
        import re
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
