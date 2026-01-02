# Quick Start Guide - Streamlit Form

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```powershell
cd c:\Users\Ranganathan.9703\Documents\last_compliance
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start the Form
```powershell
streamlit run streamlit_app.py
```

### Step 3: Submit Compliance Items
1. Open browser at `http://localhost:8501`
2. Choose tab: **ISO Certificates** or **India Compliance**
3. Fill the form and click Submit

---

## 📋 ISO Certificate Form

### Quick Fields:
- **ISO Standard**: Select from dropdown (9001, 14001, 27001, etc.)
- **Activity**: New cert, Recert, Audit, etc.
- **Email**: Person responsible
- **Due Date**: Deadline
- **Description**: Requirements details

### Example Entry:
- Standard: `ISO 9001 - Quality Management`
- Activity: `Recertification`  
- Email: `qm@company.com`
- Due Date: `2025-03-31`
- Description: `Annual ISO 9001 recertification for manufacturing unit. Need to prepare quality manual updates and process documentation.`

---

## 🇮🇳 India Compliance Form

### Quick Fields:
- **Category**: BIS, CPCB, Factory Act, Labour Laws, GST, etc.
- **State**: Select applicable state/region
- **Email**: Compliance officer
- **Due Date**: Filing/renewal deadline
- **Requirements**: What needs to be done

### Example Entry:
- Category: `Bureau of Indian Standards (BIS)`
- State: `Maharashtra`
- Email: `compliance@company.com`
- Due Date: `2025-02-28`
- Requirements: `BIS license renewal for electronics products. Need to submit test reports and factory inspection documents.`

---

## 📊 View & Process

### View Submissions:
1. Click **View Submissions** tab
2. See all pending items in table
3. Check submission count

### Process Items:
```powershell
python main.py
```

This will:
- ✅ Read all submissions
- ✅ Search for prerequisites  
- ✅ Extract requirements with AI
- ✅ Send email notifications
- ✅ Save to master list

---

## 💡 Tips

**For ISO Compliance:**
- Use specific ISO standard numbers
- Mention certification body if known
- Include scope and site location
- Note current status

**For India Compliance:**
- Specify exact state/region
- Include regulatory authority name
- Mention license numbers if applicable
- Note filing frequency and penalties

**General:**
- ⭐ Be specific in descriptions
- ⭐ Provide accurate due dates
- ⭐ Double-check email addresses
- ⭐ Use Additional Notes for context

---

## ❓ Common Questions

**Q: Can I edit a submission?**  
A: Currently, delete from View tab and resubmit

**Q: How do I know it's processed?**  
A: Check master_compliance.xlsx after running main.py

**Q: Can I submit bulk items?**  
A: Use the form multiple times or import via Excel

**Q: What if email fails?**  
A: Check logs/compliance_assistant.log for errors

---

## 🎯 Next Steps

1. ✅ Submit your first compliance item
2. ✅ Review in View Submissions tab  
3. ✅ Run `python main.py` to process
4. ✅ Check email for notification
5. ✅ Review logs for any issues

---

**Need Help?** See [STREAMLIT_FORM.md](STREAMLIT_FORM.md) for detailed documentation.
