"""
Main orchestration script for Compliance Assistant.
Coordinates the workflow from Excel ingestion to Outlook notifications.
"""
import logging
import os
from pathlib import Path
from config.logging_config import setup_logging
from utils.excel_utils import read_new_items, check_duplicate, save_to_master
from scrapers.web_search_scraper import search_prerequisites
from llm.query_handler import extract_prerequisites
from llm.retriever import store_in_vector_db
from notifications.outlook_notifier import send_notification

def save_to_text_file(item_title, prerequisites, output_path="data/output/prerequisites.txt"):
    """Save extracted prerequisites to a text file for manual verification."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"ITEM: {item_title}\n")
        f.write(f"TIMESTAMP: {Path(output_path).stat().st_mtime if output_file.exists() else 'NEW'}\n")
        f.write("-" * 40 + "\n")
        f.write(prerequisites + "\n")
        f.write("=" * 80 + "\n\n")

def main():
    """Main orchestration workflow for the Compliance Assistant."""
    # Setup logging
    logger = setup_logging()
    logger.info("=" * 80)
    logger.info("Starting Compliance Assistant workflow")
    logger.info("=" * 80)
    
    try:
        # Step 1: Read new items from Excel form
        logger.info("Step 1: Reading new compliance items from Excel")
        new_items = read_new_items("data/excel/new_submissions.xlsx")
        logger.info(f"Found {len(new_items)} new items to process")
        
        if not new_items:
            logger.info("No new items to process. Exiting.")
            return
        
        # Step 2: Process each item
        processed_count = 0
        skipped_count = 0
        error_count = 0
        
        for idx, item in enumerate(new_items, 1):
            try:
                logger.info(f"\n{'=' * 60}")
                logger.info(f"Processing item {idx}/{len(new_items)}: '{item.get('Title', 'Unknown')}'")
                logger.info(f"{'=' * 60}")
                
                # Check for duplicates
                if check_duplicate(item, "data/excel/master_compliance.xlsx"):
                    logger.info(f"Item '{item['Title']}' already exists in master list, skipping")
                    skipped_count += 1
                    continue
                
                # Step 3: Web search for prerequisites
                logger.info(f"Step 3: Searching for prerequisites: {item['Title']}")
                search_results = search_prerequisites(item['Title'], item['Description'])
                
                if not search_results:
                    logger.warning(f"No search results found for '{item['Title']}'")
                    continue
                
                # Step 4: LLM extraction
                logger.info("Step 4: Extracting prerequisites using LLM")
                prerequisites = extract_prerequisites(search_results, item)
                logger.info(f"Prerequisites extracted successfully ({len(prerequisites)} characters)")
                
                # NEW STEP: Save output to text file for verification (as requested)
                logger.info("Saving prerequisites to data/output/prerequisites.txt for verification")
                save_to_text_file(item['Title'], prerequisites)
                
                # Step 5: Store in vector DB
                logger.info("Step 5: Storing data in vector database")
                store_in_vector_db(item, prerequisites, search_results)
                
                # Step 6: Send notification
                logger.info(f"Step 6: Sending notification to {item['Responsible Email']}")
                try:
                    send_notification(
                        to_email=item['Responsible Email'],
                        subject=f"New Compliance Item: {item['Title']}",
                        prerequisites=prerequisites,
                        due_date=item['Due Date']
                    )
                except Exception as notify_err:
                    logger.warning(f"Could not send notification (skipping to next step): {str(notify_err)}")
                
                # Step 7: Save to master list
                logger.info("Step 7: Saving to master compliance list")
                save_to_master(item, prerequisites, "data/excel/master_compliance.xlsx")
                
                logger.info(f"Successfully processed: {item['Title']}")
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing item '{item.get('Title', 'Unknown')}': {str(e)}")
                error_count += 1
                continue
        
        # Final summary
        logger.info(f"\n{'=' * 80}")
        logger.info("Workflow Summary:")
        logger.info(f"  Total items: {len(new_items)}")
        logger.info(f"  Successfully processed: {processed_count}")
        logger.info(f"  Skipped (duplicates): {skipped_count}")
        logger.info(f"  Errors: {error_count}")
        logger.info("=" * 80)
        logger.info("Compliance Assistant workflow completed")
        logger.info("=" * 80)
    
    except Exception as e:
        logger.error(f"Fatal error in main workflow: {str(e)}")
        raise

if __name__ == "__main__":
    main()
