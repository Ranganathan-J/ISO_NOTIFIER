"""
Default lead times for different compliance categories.
Values are in days.
"""

ISO_LEAD_TIMES = {
    "ISO 9001 - Quality Management": 90,
    "ISO 14001 - Environmental Management": 90,
    "ISO 27001 - Information Security Management": 120,
    "ISO 45001 - Occupational Health & Safety": 90,
    "ISO 22000 - Food Safety Management": 90,
    "ISO 50001 - Energy Management": 120,
    "ISO 13485 - Medical Devices Quality Management": 120,
    "ISO 20000 - IT Service Management": 120,
}

# Activity type adjustments (add or subtract days)
ISO_ACTIVITY_ADJUSTMENTS = {
    "New Certification": 30,
    "Recertification": 0,
    "Surveillance Audit": -30,
    "Gap Analysis": -60,
    "Internal Audit Preparation": -45,
    "Document Review": -75,
    "Corrective Action Implementation": -30
}

INDIA_COMPLIANCE_LEAD_TIMES = {
    "Bureau of Indian Standards (BIS)": 180,
    "Central Pollution Control Board (CPCB)": 120,
    "Environmental Clearance": 270,
    "Factory Act Compliance": 60,
    "Labour Law Compliance": 60,
    "GST Compliance": 30,
    "Import/Export Regulations": 90,
    "Industry-Specific License": 120,
    "State-Level Compliance": 90
}

DEFAULT_LEAD_TIME = 30

def get_iso_due_date(standard_name, activity_type, start_date=None):
    """Calculate due date for ISO certification activity."""
    from datetime import datetime, timedelta
    if start_date is None:
        start_date = datetime.now()
    
    base_days = ISO_LEAD_TIMES.get(standard_name, DEFAULT_LEAD_TIME)
    adj_days = ISO_ACTIVITY_ADJUSTMENTS.get(activity_type, 0)
    
    return start_date + timedelta(days=base_days + adj_days)

def get_india_due_date(category_name, start_date=None):
    """Calculate due date for India compliance item."""
    from datetime import datetime, timedelta
    if start_date is None:
        start_date = datetime.now()
    
    days = INDIA_COMPLIANCE_LEAD_TIMES.get(category_name, DEFAULT_LEAD_TIME)
    
    return start_date + timedelta(days=days)
