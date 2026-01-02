"""
LangChain LLM client using Groq for fast inference.
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("ComplianceAssistant.LLM")

def get_llm_client(model="qwen/qwen3-32b", temperature=0.3):
    """
    Initialize and return Groq LLM client.
    
    Args:
        model: Groq model name
        temperature: Sampling temperature (0-1)
    
    Returns:
        LangChain ChatGroq instance
    """
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model,
            temperature=temperature
        )
        
        logger.info(f"Initialized Groq LLM: {model}")
        return llm
    
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise

def create_prerequisite_prompt():
    """
    Create prompt template for extracting prerequisites.
    
    Returns:
        ChatPromptTemplate for prerequisite extraction
    """
    template = """
You are a Senior Compliance Specialist and Auditor. Your task is to analyze search results and determine BOTH the technical prerequisites AND the accurate due date/expiry for a compliance item.

**Compliance Item:**
Title: {title}
Description: {description}
Application Date: {application_date} (The date the process was initiated)

**Search Results (Raw Data):**
{search_results}

**CRITICAL INSTRUCTIONS:**
1. **DETERMINE VALIDITY**: Look for the standard validity or renewal period for this certificate (e.g., is it valid for 1 year, 3 years, etc?).
2. **CALCULATE DUE DATE**: Based on the [Application Date] and the validity period found in the search results, calculate the final [Calculated Due Date]. 
   - Format it as YYYY-MM-DD.
   - If the standard says "3 years validity", the due date is Application Date + 3 years.
3. **EXTRACT PREREQUISITES**: Extract a clean, numbered list of actionable requirements from official sources.
4. **NO THINKING TAGS**: Do not include <think> or any reasoning.
5. **ACCURACY**: If official sources specify a period, use that. Do not guess.

**Output Format:**

[DUE_DATE]: YYYY-MM-DD
[VALIDITY_PERIOD]: e.g., 3 Years / Annual

Prerequisites for {title}:
1. [Requirement 1]
2. [Requirement 2]
...

Additional Notes: [Technical context only]
"""
    
    return ChatPromptTemplate.from_template(template)
