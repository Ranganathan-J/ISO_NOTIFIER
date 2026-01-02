# LangChain Packages Update Guide

## What Changed

The application has been updated to use LangChain's latest modular architecture, which splits functionality into separate, focused packages.

## Updated Package Structure

### Before (Old)
```python
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
```

### After (New - Current)
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
```

## Updated Dependencies in requirements.txt

```txt
# LLM and AI - Using latest modular LangChain packages
langchain-core>=0.1.0           # Core abstractions and interfaces
langchain-groq>=0.1.0           # Groq LLM integration
langchain-community>=0.0.38     # Community integrations (vector stores, etc.)
langchain-openai>=0.0.5         # OpenAI integrations (embeddings, chat models)
langchain-text-splitters>=0.0.1 # Text splitting utilities
chromadb>=0.4.22                # Vector database
openai>=1.12.0                  # OpenAI API client
```

## File Changes

### 1. requirements.txt
- ✅ Updated to use modular LangChain packages
- ✅ Removed deprecated `langchain` monolithic package
- ✅ Added `langchain-core`, `langchain-text-splitters`
- ✅ Updated version constraints for better compatibility

### 2. llm/llm_client.py
```python
# Changed import
from langchain_core.prompts import ChatPromptTemplate  # was: from langchain.prompts
```

### 3. llm/retriever.py
```python
# Changed imports
from langchain_text_splitters import RecursiveCharacterTextSplitter  # was: from langchain.text_splitter
from langchain_core.documents import Document  # was: from langchain.docstore.document
```

## Benefits of the Update

1. **Smaller Dependencies**: Only install what you need
2. **Faster Installation**: Modular packages are smaller and install faster
3. **Better Maintenance**: Each package is maintained and versioned separately
4. **Future-Proof**: Aligns with LangChain's official direction
5. **Clearer Organization**: Imports clearly show where functionality comes from

## Package Responsibilities

| Package | Purpose | Used For |
|---------|---------|----------|
| `langchain-core` | Core abstractions, interfaces, base classes | Prompts, Documents, base LLM interface |
| `langchain-community` | Community integrations | Vector stores (Chroma), community tools |
| `langchain-groq` | Groq provider | ChatGroq LLM integration |
| `langchain-openai` | OpenAI provider | OpenAI embeddings and chat models |
| `langchain-text-splitters` | Text processing | Document chunking and splitting |

## Installation

After these changes, install dependencies with:

```powershell
# Activate virtual environment
venv\Scripts\activate

# Install/upgrade all packages
pip install -r requirements.txt --upgrade
```

## Migration Notes

### No Breaking Changes to Application Logic
- The actual functionality remains the same
- Only import statements changed
- No changes to API or method signatures
- All existing code continues to work

### Key Differences

1. **Prompts**: Now in `langchain_core.prompts`
   - `ChatPromptTemplate`, `PromptTemplate`, etc.

2. **Documents**: Now in `langchain_core.documents`
   - `Document` class for vector store operations

3. **Text Splitters**: Now in `langchain_text_splitters`
   - `RecursiveCharacterTextSplitter`, `CharacterTextSplitter`, etc.

4. **Vector Stores**: Still in `langchain_community.vectorstores`
   - `Chroma`, `FAISS`, `Pinecone`, etc.

## Verification

To verify the updates are working correctly:

```powershell
# Test imports
python -c "from langchain_core.prompts import ChatPromptTemplate; print('✓ langchain-core')"
python -c "from langchain_groq import ChatGroq; print('✓ langchain-groq')"
python -c "from langchain_community.vectorstores import Chroma; print('✓ langchain-community')"
python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; print('✓ langchain-text-splitters')"
```

## Troubleshooting

### "No module named 'langchain_core'"

```powershell
pip install langchain-core langchain-community langchain-text-splitters
```

### "ImportError: cannot import name 'ChatPromptTemplate'"

Make sure you're importing from the correct package:
```python
# ✓ Correct
from langchain_core.prompts import ChatPromptTemplate

# ✗ Wrong (deprecated)
from langchain.prompts import ChatPromptTemplate
```

### Dependency Conflicts

```powershell
# Clean install
pip uninstall langchain langchain-core langchain-community langchain-groq langchain-openai langchain-text-splitters -y
pip install -r requirements.txt
```

## References

- [LangChain Python Docs](https://python.langchain.com/)
- [LangChain Core Documentation](https://python.langchain.com/docs/langchain_core/)
- [Migration Guide](https://python.langchain.com/docs/versions/migrating_chains/)
