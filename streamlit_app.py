import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import os
import sys

# Add project root to path so we can import internal modules
sys.path.append(os.path.abspath(os.curdir))

from scrapers.web_search_scraper import search_prerequisites
from llm.query_handler import extract_prerequisites
from llm.retriever import store_in_vector_db
# from utils.compliance_mappings import get_iso_due_date, get_india_due_date

# Configure page
st.set_page_config(
    page_title="ISO Compliance Assistant",
    page_icon="📋",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0078d4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #0078d4;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        border-bottom: 2px solid #0078d4;
        padding-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.25rem;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏢 ISO Compliance Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #605e5c;">Submit compliance items for ISO certificates and India regulatory requirements</p>', unsafe_allow_html=True)
# Info box
st.markdown("""
<div class="info-box">
    <strong>📌 Instructions:</strong> Fill in the form below to submit a new compliance item. 
    All fields marked with * are required. The system will automatically research prerequisites 
    and send notifications to the responsible person.
</div>
""", unsafe_allow_html=True)

# Helper function to process the compliance item in real-time
def process_compliance_item(title, description, application_date, email, category):
    """Run web search and LLM extraction in real-time."""
    with st.spinner(f"🔍 Researching prerequisites and expiry for {title}..."):
        try:
            # 1. Search for prerequisites
            search_results = search_prerequisites(title, description)
            
            if not search_results:
                st.warning("⚠️ No specific prerequisites found online. Try providing more details.")
                return None
            
            # 2. Extract with LLM
            item_data = {
                'Title': title,
                'Description': description,
                'Application Date': str(application_date),
                'Responsible Email': email
            }
            
            result = extract_prerequisites(search_results, item_data)
            
            # Extract new due date from LLM result if present
            # result is now a dict or a string with tags
            # We'll update the handler to return a structured dict
            
            # 3. Store in Vector DB (optional/background)
            try:
                # store_in_vector_db expects string for prerequisites
                prereqs_text = result.get('prerequisites', str(result))
                store_in_vector_db(item_data, prereqs_text, search_results)
            except Exception as e:
                st.error(f"Error storing in vector DB: {str(e)}")
            
            return result
            
        except Exception as e:
            st.error(f"❌ Error during processing: {str(e)}")
            return None

# Helper function to save data (defined before tabs so it's available)
def save_to_excel(title, description, email, due_date, category, application_date):
    """Save compliance item to Excel file."""
    excel_path = "data/excel/new_submissions.xlsx"
    
    # Ensure directory exists
    Path(excel_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Create new row
    new_row = {
        'Title': f"[{category}] {title}",
        'Description': description,
        'Responsible Email': email,
        'Application Date': application_date.strftime('%Y-%m-%d'),
        'Due Date': due_date.strftime('%Y-%m-%d'),
        'Submitted At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Load existing or create new DataFrame
    if Path(excel_path).exists():
        try:
            df = pd.read_excel(excel_path)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        except Exception:
            df = pd.DataFrame([new_row])
    else:
        df = pd.DataFrame([new_row])
    
    # Save to Excel
    df.to_excel(excel_path, index=False)

# Create tabs for different compliance types
tab1, tab2, tab3 = st.tabs(["📜 ISO Certificates", "🇮🇳 India Compliance", "📊 View Submissions"])

with tab1:
    st.markdown('<h2 class="section-header">ISO Certificate Compliance</h2>', unsafe_allow_html=True)
    
    with st.form("iso_compliance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            iso_standard = st.selectbox(
                "ISO Standard *",
                [
                    "ISO 9001 - Quality Management",
                    "ISO 14001 - Environmental Management",
                    "ISO 27001 - Information Security Management",
                    "ISO 45001 - Occupational Health & Safety",
                    "ISO 22000 - Food Safety Management",
                    "ISO 50001 - Energy Management",
                    "ISO 13485 - Medical Devices Quality Management",
                    "ISO 20000 - IT Service Management",
                    "Other ISO Standard"
                ]
            )
            
            if iso_standard == "Other ISO Standard":
                custom_iso = st.text_input("Specify ISO Standard *")
                title = custom_iso
            else:
                title = iso_standard
            
            certification_type = st.selectbox(
                "Activity Type *",
                [
                    "New Certification",
                    "Recertification",
                    "Surveillance Audit",
                    "Gap Analysis",
                    "Internal Audit Preparation",
                    "Document Review",
                    "Corrective Action Implementation"
                ]
            )
        
        with col2:
            responsible_email = st.text_input("Responsible Person Email *", placeholder="user@company.com")
            
            application_date = st.date_input(
                "Application Date *",
                value=datetime.now().date(),
                help="The date when the certification process or application was initiated.",
                key="iso_app_date"
            )
            
            # Application Date for backend processing
            application_date_dt = datetime.combine(application_date, datetime.min.time())
            
            # The due date is now autogenerated by LLM, so we don't calculate it here anymore
            due_date = None 
            # due_date = st.date_input(
            #     "Due Date (Auto-calculated) *",
            #     value=calculated_due_date.date(),
            #     min_value=datetime.now().date(),
            #     help="Automatically calculated based on standard and activity type. You can adjust if needed."
            # )
            
            priority = st.selectbox(
                "Priority",
                ["Critical", "High", "Medium", "Low"]
            )
        
        st.markdown("---")
        
        description = st.text_area(
            "Description / Requirements *",
            placeholder="Describe the compliance requirements, scope, and any specific details...",
            height=150
        )
        
        # Additional ISO-specific fields
        st.markdown("**Additional Details**")
        col3, col4 = st.columns(2)
        
        with col3:
            scope = st.text_input("Scope of Certification", placeholder="e.g., Manufacturing operations")
            location = st.text_input("Location / Site", placeholder="e.g., Mumbai Plant")
        
        with col4:
            certification_body = st.text_input("Certification Body", placeholder="e.g., Bureau Veritas, TUV")
            current_status = st.selectbox(
                "Current Status",
                ["Not Started", "In Progress", "Documentation Ready", "Audit Scheduled", "Pending Closure"]
            )
        
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any other relevant information...",
            height=100
        )
        
        submitted1 = st.form_submit_button("Submit ISO Compliance Item", type="primary", use_container_width=True)
        
    # Results containers (persistence across reruns)
    if 'iso_results' not in st.session_state:
        st.session_state.iso_results = None
    if 'india_results' not in st.session_state:
        st.session_state.india_results = None

    if submitted1:
        if not all([title, responsible_email, description]):
            st.error("❌ Please fill in all required fields (marked with *)")
        elif "@" not in responsible_email:
            st.error("❌ Please enter a valid email address")
        else:
            # Create comprehensive description
            full_description = f"""
**Activity Type:** {certification_type}
**Scope:** {scope or 'Not specified'}
**Location:** {location or 'Not specified'}
**Certification Body:** {certification_body or 'TBD'}
**Current Status:** {current_status}
**Priority:** {priority}

**Requirements:**
{description}

**Additional Notes:**
{notes or 'None'}
"""
            
            # RUN WORKFLOW IN REAL TIME
            llm_result = process_compliance_item(title, description, application_date, responsible_email, "ISO")
            
            # Use LLM-calculated due date
            final_due_date_str = llm_result.get('due_date', 'TBD')
            # Try to convert to datetime for Excel if valid
            try:
                final_due_date_obj = datetime.strptime(final_due_date_str, '%Y-%m-%d')
            except:
                final_due_date_obj = application_date + timedelta(days=365) # Fallback 1 year
            
            # Save to Excel AFTER getting LLM result for accurate due date
            save_to_excel(title, full_description.strip(), responsible_email, final_due_date_obj, "ISO", application_date)
            st.success("✅ ISO compliance item submitted and processed successfully!")
            
            st.session_state.iso_results = {
                'title': title,
                'due_date': final_due_date_str,
                'prerequisites': llm_result.get('prerequisites', ''),
                'validity': llm_result.get('validity', 'Not determined')
            }
            st.balloons()
            
    # Display ISO results if they exist in session state
    if st.session_state.iso_results:
        res = st.session_state.iso_results
        st.markdown("---")
        st.markdown(f"### 📋 Extracted Prerequisites for: {res['title']}")
        
        # Display due date intelligence
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Final Due Date", res['due_date'])
        with col_res2:
            st.metric("Validity Period", res.get('validity', 'N/A'))
        with col_res3:
            conf = res.get('confidence', 0)
            st.metric("Calculation Confidence", f"{conf:.1%}")

        # Technical Notes
        with st.expander("🔍 Date Intelligence & Methodology"):
            st.write(f"**Method:** {res.get('calculation_method', 'Unknown').replace('_', ' ').title()}")
            st.write(f"**Notes:** {res.get('calculation_notes', 'No notes available.')}")
            if res.get('warning'):
                st.warning(f"⚠️ {res['warning']}")
        
        if res['prerequisites']:
            st.info("These prerequisites were researched and extracted using web search + AI.")
            st.markdown(res['prerequisites'])
            
            st.download_button(
                label="📥 Download Prerequisites as TXT",
                data=res['prerequisites'],
                file_name=f"prerequisites_{res['title'].replace(' ', '_')}.txt",
                mime="text/plain",
                key="download_iso"
            )
        else:
            st.warning("No prerequisites were extracted.")

with tab2:
    st.markdown('<h2 class="section-header">India-Specific Compliance</h2>', unsafe_allow_html=True)
    
    with st.form("india_compliance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            compliance_category = st.selectbox(
                "Compliance Category *",
                [
                    "Bureau of Indian Standards (BIS)",
                    "Central Pollution Control Board (CPCB)",
                    "Environmental Clearance",
                    "Factory Act Compliance",
                    "Labour Law Compliance",
                    "GST Compliance",
                    "Import/Export Regulations",
                    "Industry-Specific License",
                    "State-Level Compliance",
                    "Other Regulatory Requirement"
                ]
            )
            
            if compliance_category == "Other Regulatory Requirement":
                custom_category = st.text_input("Specify Compliance Category *")
                india_title = custom_category
            else:
                india_title = compliance_category
            
            state = st.selectbox(
                "State",
                [
                    "All India", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
                    "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
                    "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
                    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
                    "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
                    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
                    "Delhi", "Jammu & Kashmir", "Ladakh", "Puducherry"
                ]
            )
        
        with col2:
            india_email = st.text_input("Responsible Person Email *", placeholder="compliance@company.com")
            
            india_application_date = st.date_input(
                "Application Date *",
                value=datetime.now().date(),
                help="The date when the compliance process or application was initiated.",
                key="india_app_date"
            )
            
            # Date for backend processing
            india_app_date_dt = datetime.combine(india_application_date, datetime.min.time())
            
            # The due date is now autogenerated by LLM
            india_due_date = None
            # india_due_date = st.date_input(
            #     "Compliance Due Date (Auto-calculated) *",
            #     value=calculated_india_due_date.date(),
            #     min_value=datetime.now().date(),
            #     help="Automatically calculated based on compliance category. You can adjust if needed."
            # )
            
            filing_frequency = st.selectbox(
                "Filing Frequency",
                ["One-time", "Annual", "Quarterly", "Monthly", "As Required"]
            )
        
        st.markdown("---")
        
        india_description = st.text_area(
            "Compliance Requirements *",
            placeholder="Describe the regulatory requirements, documentation needed, and compliance steps...",
            height=150
        )
        
        # India-specific fields
        st.markdown("**Regulatory Details**")
        col5, col6 = st.columns(2)
        
        with col5:
            authority = st.text_input("Regulatory Authority", placeholder="e.g., State Pollution Control Board")
            license_number = st.text_input("License/Certificate Number", placeholder="If applicable")
        
        with col6:
            penalty_info = st.text_input("Penalty for Non-Compliance", placeholder="e.g., Fine, Imprisonment")
            renewal_required = st.selectbox("Renewal Required", ["No", "Yes - Annual", "Yes - Biennial", "Yes - Other"])
        
        india_notes = st.text_area(
            "Additional Information",
            placeholder="Reference documents, previous compliance records, etc.",
            height=100
        )
        
        submitted2 = st.form_submit_button("Submit India Compliance Item", type="primary", use_container_width=True)
        
    if submitted2:
        if not all([india_title, india_email, india_description]):
            st.error("❌ Please fill in all required fields (marked with *)")
        elif "@" not in india_email:
            st.error("❌ Please enter a valid email address")
        else:
            # Create comprehensive description
            india_full_description = f"""
**Category:** {compliance_category}
**State/Region:** {state}
**Regulatory Authority:** {authority or 'Not specified'}
**License Number:** {license_number or 'N/A'}
**Filing Frequency:** {filing_frequency}
**Renewal:** {renewal_required}
**Penalty:** {penalty_info or 'Not specified'}

**Requirements:**
{india_description}

**Additional Information:**
{india_notes or 'None'}
"""
            
            # RUN WORKFLOW IN REAL TIME
            llm_result = process_compliance_item(india_title, india_description, india_application_date, india_email, "India")
            
            # Use LLM-calculated due date
            final_india_due_date_str = llm_result.get('due_date', 'TBD')
            try:
                final_india_due_date_obj = datetime.strptime(final_india_due_date_str, '%Y-%m-%d')
            except:
                final_india_due_date_obj = india_application_date + timedelta(days=365) # Fallback
            
            # Save to Excel AFTER getting LLM result
            save_to_excel(india_title, india_full_description.strip(), india_email, final_india_due_date_obj, "India", india_application_date)
            st.success("✅ India compliance item submitted and processed successfully!")
            
            st.session_state.india_results = {
                'title': india_title,
                'due_date': final_india_due_date_str,
                'prerequisites': llm_result.get('prerequisites', ''),
                'validity': llm_result.get('validity', 'Not determined')
            }
            st.balloons()

    # Display India results if they exist in session state
    if st.session_state.india_results:
        res = st.session_state.india_results
        st.markdown("---")
        st.markdown(f"### 📋 Extracted Prerequisites for: {res['title']}")
        
        # Display due date intelligence
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("Final Due Date", res['due_date'])
        with col_res2:
            st.metric("Validity Period", res.get('validity', 'N/A'))
        with col_res3:
            conf = res.get('confidence', 0)
            st.metric("Calculation Confidence", f"{conf:.1%}")

        # Technical Notes
        with st.expander("🔍 Date Intelligence & Methodology"):
            st.write(f"**Method:** {res.get('calculation_method', 'Unknown').replace('_', ' ').title()}")
            st.write(f"**Notes:** {res.get('calculation_notes', 'No notes available.')}")
            if res.get('warning'):
                st.warning(f"⚠️ {res['warning']}")
        
        if res['prerequisites']:
            st.info("These prerequisites were researched and extracted using web search + AI.")
            st.markdown(res['prerequisites'])
            
            st.download_button(
                label="📥 Download Prerequisites as TXT",
                data=res['prerequisites'],
                file_name=f"prerequisites_india_{res['title'].replace(' ', '_')}.txt",
                mime="text/plain",
                key="download_india"
            )
        else:
            st.warning("No prerequisites were extracted.")

with tab3:
    st.markdown('<h2 class="section-header">Recent Submissions</h2>', unsafe_allow_html=True)
    
    # Load and display existing submissions
    excel_path = "data/excel/new_submissions.xlsx"
    
    if Path(excel_path).exists():
        try:
            df = pd.read_excel(excel_path)
            
            if not df.empty:
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown("---")
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.metric("Total Submissions", len(df))
                with col_b:
                    if st.button("🗑️ Clear All Submissions", help="This will delete all pending submissions"):
                        os.remove(excel_path)
                        st.success("All submissions cleared!")
                        st.rerun()
            else:
                st.info("📝 No submissions yet. Use the forms above to add compliance items.")
        except Exception as e:
            st.error(f"Error loading submissions: {str(e)}")
    else:
        st.info("📝 No submissions yet. Use the forms above to add compliance items.")

# Sidebar information
with st.sidebar:
    st.markdown("### 📚 Quick Reference")
    
    st.markdown("""
    **Common ISO Standards:**
    - **ISO 9001**: Quality Management
    - **ISO 14001**: Environmental
    - **ISO 27001**: Information Security
    - **ISO 45001**: Health & Safety
    
    **India Compliance:**
    - BIS Certification
    - CPCB Requirements
    - Factory Act
    - Labour Laws
    """)
    
    st.markdown("---")
    st.markdown("### 📞 Support")
    st.markdown("For assistance, contact:")
    st.markdown("📧 compliance@company.com")
    
    st.markdown("---")
    st.markdown("### ⚙️ Actions")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.button("🚀 Process Submissions"):
        st.info("Run `python main.py` to process submissions and send notifications.")
