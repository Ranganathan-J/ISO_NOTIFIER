"""
Excel utilities for reading, writing, and managing compliance data.
"""
import pandas as pd
from pathlib import Path
import hashlib
import logging

logger = logging.getLogger("ComplianceAssistant.ExcelUtils")

def read_new_items(file_path):
    """
    Read new compliance items from Excel submission form.
    
    Args:
        file_path: Path to Excel file with new submissions
    
    Returns:
        List of dictionaries containing item data
    """
    try:
        df = pd.read_excel(file_path)
        
        # Validate required columns
        required_cols = ['Title', 'Description', 'Responsible Email', 'Due Date']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Convert to list of dictionaries
        items = df.to_dict('records')
        logger.info(f"Successfully read {len(items)} items from {file_path}")
        return items
    
    except Exception as e:
        logger.error(f"Error reading Excel file {file_path}: {str(e)}")
        raise

def check_duplicate(item, master_file):
    """
    Check if an item already exists in the master compliance list.
    
    Args:
        item: Dictionary containing item data
        master_file: Path to master compliance Excel file
    
    Returns:
        True if duplicate exists, False otherwise
    """
    try:
        # Create hash of title + description for exact matching
        item_hash = hashlib.md5(
            f"{item['Title']}{item['Description']}".encode()
        ).hexdigest()
        
        # Read master file if it exists
        if not Path(master_file).exists():
            logger.info("Master file doesn't exist, creating new one")
            return False
        
        df = pd.read_excel(master_file)
        
        # Check if hash column exists
        if 'Item Hash' in df.columns:
            return item_hash in df['Item Hash'].values
        
        # Fallback: check title match
        return item['Title'] in df['Title'].values
    
    except Exception as e:
        logger.error(f"Error checking duplicates: {str(e)}")
        return False

def save_to_master(item, prerequisites, master_file):
    """
    Save processed item to master compliance list.
    
    Args:
        item: Dictionary containing item data
        prerequisites: Extracted prerequisites text
        master_file: Path to master compliance Excel file
    """
    try:
        # Create item hash
        item_hash = hashlib.md5(
            f"{item['Title']}{item['Description']}".encode()
        ).hexdigest()
        
        # Prepare new row
        new_row = {
            'Title': item['Title'],
            'Description': item['Description'],
            'Responsible Email': item['Responsible Email'],
            'Due Date': item['Due Date'],
            'Prerequisites': prerequisites,
            'Item Hash': item_hash,
            'Status': 'Notified'
        }
        
        # Read existing or create new DataFrame
        if Path(master_file).exists():
            df = pd.read_excel(master_file)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df = pd.DataFrame([new_row])
        
        # Save to Excel
        Path(master_file).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(master_file, index=False)
        logger.info(f"Saved item '{item['Title']}' to master list")
    
    except Exception as e:
        logger.error(f"Error saving to master file: {str(e)}")
        raise
