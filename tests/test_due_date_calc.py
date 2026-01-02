import pytest
from datetime import datetime, timedelta
from utils.compliance_mappings import get_iso_due_date, get_india_due_date

def test_iso_due_date_calculation():
    # Test ISO 9001 with New Certification
    start_date = datetime(2025, 1, 1)
    # 90 (base) + 30 (new cert) = 120 days
    expected_date = start_date + timedelta(days=120)
    assert get_iso_due_date("ISO 9001 - Quality Management", "New Certification", start_date) == expected_date

    # Test ISO 27001 with Surveillance Audit
    # 120 (base) - 30 (audit) = 90 days
    expected_date = start_date + timedelta(days=90)
    assert get_iso_due_date("ISO 27001 - Information Security Management", "Surveillance Audit", start_date) == expected_date

def test_india_due_date_calculation():
    start_date = datetime(2025, 1, 1)
    # BIS: 180 days
    expected_date = start_date + timedelta(days=180)
    assert get_india_due_date("Bureau of Indian Standards (BIS)", start_date) == expected_date

    # GST: 30 days
    expected_date = start_date + timedelta(days=30)
    assert get_india_due_date("GST Compliance", start_date) == expected_date
