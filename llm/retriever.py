"""
Vector store setup for semantic search and retrieval using ChromaDB.
"""
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("ComplianceAssistant.Retriever")

def get_vector_store(persist_directory="data/vector_store"):
    """
    Initialize or load existing vector store using free Hugging Face embeddings.
    
    Args:
        persist_directory: Directory to persist vector store
    
    Returns:
        Chroma vector store instance
    """
    try:
        # Use a free, high-quality local embedding model
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        vector_store = Chroma(
            collection_name="compliance_items",
            embedding_function=embeddings,
            persist_directory=persist_directory
        )
        
        logger.info(f"Initialized vector store at {persist_directory} using {model_name}")
        return vector_store
    
    except Exception as e:
        logger.error(f"Error initializing vector store: {str(e)}")
        raise

def store_in_vector_db(item, prerequisites, search_results):
    """
    Store compliance item and prerequisites in vector database.
    
    Args:
        item: Compliance item dictionary
        prerequisites: Extracted prerequisites text
        search_results: Original search results
    """
    try:
        vector_store = get_vector_store()
        
        # Create documents for vector store
        documents = []
        
        # Main compliance item document
        main_doc = Document(
            page_content=f"Title: {item['Title']}\nDescription: {item['Description']}\nPrerequisites: {prerequisites}",
            metadata={
                "type": "compliance_item",
                "title": item['Title'],
                "responsible_email": item['Responsible Email'],
                "due_date": str(item['Due Date'])
            }
        )
        documents.append(main_doc)
        
        # Add search results as separate documents
        for idx, result in enumerate(search_results):
            if result.get('content'):
                doc = Document(
                    page_content=result['content'],
                    metadata={
                        "type": "source_document",
                        "title": result['title'],
                        "url": result['url'],
                        "related_to": item['Title']
                    }
                )
                documents.append(doc)
        
        # Split documents if needed
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Add to vector store
        vector_store.add_documents(split_docs)
        logger.info(f"Stored {len(split_docs)} document chunks in vector DB")
    
    except Exception as e:
        logger.error(f"Error storing in vector DB: {str(e)}")

def query_vector_store(query, k=5):
    """
    Query vector store for similar compliance items.
    
    Args:
        query: Search query
        k: Number of results to return
    
    Returns:
        List of relevant documents
    """
    try:
        vector_store = get_vector_store()
        results = vector_store.similarity_search(query, k=k)
        logger.info(f"Found {len(results)} similar documents")
        return results
    
    except Exception as e:
        logger.error(f"Error querying vector store: {str(e)}")
        return []
