import os, requests

DASHBOARD_URL = os.getenv("WAZUH_DASHBOARD_URL", "https://localhost")

def test_api_status():
    url = DASHBOARD_URL.rstrip('/') + '/api/status'
    r = requests.get(url, timeout=20, verify=False)
    assert r.status_code == 200
