"""
Unit tests for Outlook notification module.
"""
import pytest
from notifications.outlook_notifier import OutlookNotifier

def test_outlook_notifier_init(mocker):
    """Test OutlookNotifier initialization."""
    # Mock environment variables
    mocker.patch.dict('os.environ', {
        'AZURE_CLIENT_ID': 'test-client-id',
        'AZURE_CLIENT_SECRET': 'test-secret',
        'AZURE_TENANT_ID': 'test-tenant-id',
        'SENDER_EMAIL': 'test@example.com'
    })
    
    # Mock MSAL
    mock_app = mocker.Mock()
    mock_app.acquire_token_for_client.return_value = {'access_token': 'test-token'}
    mocker.patch('msal.ConfidentialClientApplication', return_value=mock_app)
    
    notifier = OutlookNotifier()
    assert notifier.token == 'test-token'

def test_send_email(mocker):
    """Test email sending functionality."""
    # This would need proper mocking of MSAL and requests
    pass
