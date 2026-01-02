# Compliance Assistant

A production-ready Python application that helps compliance teams track prerequisites and notifications for compliance items using LLMs, web scraping, and Outlook integration.

## 🎯 Features

- **Excel-based Submission**: Compliance team submits items via Excel forms
- **Intelligent Deduplication**: Automatically detects and skips duplicate items
- **Web Research**: Uses DuckDuckGo to find relevant compliance prerequisites
- **AI-Powered Analysis**: LangChain + Groq LLM extracts and summarizes prerequisites
- **Vector Storage**: ChromaDB stores enriched data for semantic search
- **Outlook Notifications**: Automated email notifications via Microsoft Graph API
- **Production-Ready**: Comprehensive logging, error handling, and testing

## 📋 Prerequisites

- Python 3.11 or higher
- Microsoft Azure AD application (for Outlook integration)
- Groq API key (for LLM)
- OpenAI API key (for embeddings)

## 🚀 Setup

### 1. Create Virtual Environment

```powershell
# Navigate to project directory
cd c:\Users\Ranganathan.9703\Documents\last_compliance

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.template` to `.env` and fill in your credentials:

```bash
cp .env.template .env
```

Edit `.env` with your actual credentials:

```env
# Microsoft Azure AD (from Azure Portal)
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
SENDER_EMAIL=your-email@domain.com

# API Keys
GROQ_API_KEY=your-groq-api-key
OPENAI_API_KEY=your-openai-api-key
```

### 4. Prepare Excel Templates

The application expects compliance items in `data/excel/new_submissions.xlsx` with the following columns:

- **Title**: Compliance item title
- **Description**: Detailed description
- **Responsible Email**: Email of the person responsible
- **Due Date**: Deadline for compliance

You can use `forms/form_template.xlsx` as a starting template.

## 📁 Project Structure

```
compliance_assistant/
├── config/              # Configuration files
│   ├── config.yaml      # Application settings
│   └── logging_config.py
├── data/
│   ├── excel/          # Excel files
│   ├── raw/            # Raw scraped data
│   ├── processed/      # Processed data
│   └── vector_store/   # ChromaDB storage
├── llm/                # LLM integration
│   ├── llm_client.py
│   ├── query_handler.py
│   └── retriever.py
├── notifications/      # Email notifications
│   └── outlook_notifier.py
├── scrapers/          # Web scraping
│   └── web_search_scraper.py
├── utils/             # Utilities
│   ├── excel_utils.py
│   ├── data_cleaning.py
│   └── helpers.py
├── tests/             # Unit tests
├── main.py            # Main orchestrator
└── requirements.txt
```

## 🎮 Usage

### Option 1: Use Streamlit Web Form (Recommended)

```powershell
# Start the web form
streamlit run streamlit_app.py
```

This opens a user-friendly web interface at `http://localhost:8501` where you can:
- Submit ISO certificate compliance items
- Submit India-specific regulatory requirements  
- View all pending submissions
- Clear processed items

**Features:**
- 📜 ISO Standards: 9001, 14001, 27001, 45001, and more
- 🇮🇳 India Compliance: BIS, CPCB, Factory Act, Labour Laws, GST, etc.
- ✅ Form validation and helpful tooltips
- 📊 Real-time submission tracking

See [STREAMLIT_FORM.md](STREAMLIT_FORM.md) for detailed form documentation.

### Option 2: Manual Excel Entry

Create entries directly in `data/excel/new_submissions.xlsx` with columns:
- Title
- Description  
- Responsible Email
- Due Date

### Process Submissions

After submitting items (via web form or Excel), run:

```powershell
python main.py
```

This will:
1. Read new items from `data/excel/new_submissions.xlsx`
2. Check for duplicates in `data/excel/master_compliance.xlsx`
3. Search the web for prerequisites
4. Use LLM to extract and format prerequisites
5. Store data in vector database
6. Send email notifications to responsible persons
7. Save processed items to master list

### Run Tests

```powershell
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test file
pytest tests/test_utils.py
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

- Excel file paths
- Search parameters (max results, timeout)
- LLM settings (model, temperature)
- Vector store configuration
- Email notification settings
- Logging preferences

## 📊 Logging

Logs are stored in `logs/compliance_assistant.log` with automatic rotation:
- Maximum file size: 10 MB
- Backup count: 5 files
- Console output: INFO level
- File output: DEBUG level

## 🔐 Security

- Never commit `.env` file to version control
- Keep API keys and credentials secure
- Validate all user inputs
- Use environment variables for all secrets

## 🛠️ Development

### Module Development Order

1. **Utils**: Excel, data cleaning (no dependencies)
2. **Scraper**: Web search (depends on utils)
3. **LLM**: Client and query handler
4. **Vector Store**: ChromaDB integration
5. **Notifier**: Outlook integration
6. **Main**: Orchestrator (depends on all)

### Testing Strategy

- Write unit tests for each module
- Mock external dependencies (APIs, LLM)
- Aim for 80%+ code coverage
- Test error scenarios

## 📖 API Documentation

### Excel Utils

```python
from utils.excel_utils import read_new_items, check_duplicate, save_to_master

# Read submissions
items = read_new_items("path/to/file.xlsx")

# Check duplicates
is_duplicate = check_duplicate(item, "master.xlsx")

# Save to master
save_to_master(item, prerequisites, "master.xlsx")
```

### Web Scraper

```python
from scrapers.web_search_scraper import search_prerequisites

results = search_prerequisites("GDPR Compliance", "Data protection requirements")
```

### LLM Query Handler

```python
from llm.query_handler import extract_prerequisites

prerequisites = extract_prerequisites(search_results, item)
```

### Outlook Notifier

```python
from notifications.outlook_notifier import send_notification

send_notification(
    to_email="user@example.com",
    subject="New Compliance Item",
    prerequisites=prerequisites_text,
    due_date="2024-12-31"
)
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add/update tests
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is proprietary and confidential.

## 🆘 Troubleshooting

### Common Issues

**Import Errors**: Make sure virtual environment is activated and all dependencies are installed.

**Authentication Errors**: Verify Azure AD credentials in `.env` file.

**API Rate Limits**: Adjust `rate_limit_delay` in `config.yaml`.

**Missing Excel Files**: Ensure `data/excel/new_submissions.xlsx` exists and follows the template.

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Groq API](https://console.groq.com/docs)
- [Microsoft Graph API](https://learn.microsoft.com/en-us/graph/api/overview)
- [ChromaDB](https://docs.trychroma.com/)

## 👥 Support

For questions or issues, contact the compliance team or open an issue in the project repository.

---

**Built with ❤️ for efficient compliance management**
