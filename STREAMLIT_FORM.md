# Streamlit Compliance Form

## Overview

A web-based form interface for submitting ISO certificate and India compliance items. This replaces manual Excel entry with a user-friendly web interface.

## Features

### 📜 ISO Certificate Tab
- ISO standard selection (9001, 14001, 27001, 45001, etc.)
- Activity type (New certification, Recertification, Audit, etc.)
- Scope and location tracking
- Certification body information
- Priority levels
- Status tracking

### 🇮🇳 India Compliance Tab
- Major compliance categories:
  - Bureau of Indian Standards (BIS)
  - Central Pollution Control Board (CPCB)
  - Environmental Clearance
  - Factory Act & Labour Laws
  - GST Compliance
  - State-level requirements
- State/region selection (all Indian states)
- Regulatory authority tracking
- Filing frequency
- Penalty information
- License/certificate tracking

### 📊 View Submissions Tab
- Real-time view of all pending submissions
- Summary metrics
- Clear/delete functionality

## Installation

Already included in `requirements.txt`:
```txt
streamlit>=1.30.0
```

Install if needed:
```powershell
pip install streamlit
```

## Running the Form

```powershell
# Activate virtual environment
venv\Scripts\activate

# Run Streamlit app
streamlit run streamlit_app.py
```

The form will open in your default browser at `http://localhost:8501`

## Usage Workflow

1. **Open the Streamlit form** in your browser
2. **Select the appropriate tab**:
   - ISO Certificates for ISO compliance items
   - India Compliance for regulatory requirements
3. **Fill in the form fields**:
   - All fields marked with * are required
   - Select appropriate categories and options
   - Provide detailed descriptions
4. **Submit the form**
   - Data is saved to `data/excel/new_submissions.xlsx`
5. **Process submissions**:
   - Run `python main.py` to process the items
   - System will research prerequisites and send notifications

## Data Storage

Forms save to: `data/excel/new_submissions.xlsx`

Format:
| Title | Description | Responsible Email | Due Date | Submitted At |
|-------|-------------|-------------------|----------|--------------|
| [ISO] ISO 9001 | ... | user@company.com | 2025-01-31 | 2025-12-29 12:40 |

The `main.py` orchestrator automatically reads this file and processes all items.

## Form Fields

### ISO Compliance Form

**Required:**
- ISO Standard selection
- Activity type
- Responsible email
- Due date
- Description

**Optional:**
- Scope of certification
- Location/Site
- Certification body
- Current status
- Priority
- Additional notes

### India Compliance Form

**Required:**
- Compliance category
- Responsible email
- Due date
- Requirements description

**Optional:**
- State/Region
- Regulatory authority
- License number
- Filing frequency
- Renewal requirements
- Penalty information
- Additional notes

## Integration with Main Workflow

The Streamlit form is fully integrated with the existing workflow:

```
┌─────────────────────┐
│  Streamlit Form     │
│  (Web Interface)    │
└──────────┬──────────┘
           │ Saves to
           ▼
┌─────────────────────┐
│ new_submissions.xlsx│
└──────────┬──────────┘
           │ Read by
           ▼
┌─────────────────────┐
│    main.py          │
│  (Orchestrator)     │
└──────────┬──────────┘
           │
           ├─► Web Search (DuckDuckGo)
           ├─► LLM Extraction (Groq)
           ├─► Vector Store (ChromaDB)
           └─► Email Notification (Outlook)
```

## Customization

### Adding New ISO Standards

Edit the `iso_standard` selectbox in `streamlit_app.py`:
```python
iso_standard = st.selectbox(
    "ISO Standard *",
    [
        "ISO 9001 - Quality Management",
        "Your New Standard Here",
        ...
    ]
)
```

### Adding New India Compliance Categories

Edit the `compliance_category` selectbox:
```python
compliance_category = st.selectbox(
    "Compliance Category *",
    [
        "Bureau of Indian Standards (BIS)",
        "Your New Category Here",
        ...
    ]
)
```

### Modifying Form Layout

The form uses Streamlit's column layout:
- `col1, col2 = st.columns(2)` creates two equal columns
- Adjust weights: `st.columns([2, 1])` for 2:1 ratio
- Add more columns as needed

## Screenshots Reference

The form includes:
- Professional blue theme (#0078d4)
- Clear section headers
- Tabbed interface for different compliance types
- Success/error messages with color coding
- Info boxes for instructions
- Sidebar with quick reference and support info

## Troubleshooting

### Form doesn't open
```powershell
# Check if streamlit is installed
pip show streamlit

# Reinstall if needed
pip install streamlit --upgrade
```

### Data not saving
- Ensure `data/excel/` directory exists
- Check file permissions
- Verify openpyxl is installed: `pip install openpyxl`

### Port already in use
```powershell
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

## Tips

1. **Keep the form open** while submitting multiple items
2. **Use the View Submissions tab** to verify data before processing
3. **Process regularly**: Run `python main.py` periodically to handle submissions
4. **Clear processed items**: After main.py processes successfully, clear the submissions

## Future Enhancements

Possible additions:
- File upload for supporting documents
- Draft save functionality
- Edit/delete individual entries
- User authentication
- Email preview before submission
- Batch import from CSV
- Export to different formats
