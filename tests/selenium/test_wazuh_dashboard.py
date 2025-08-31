import os, pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DASHBOARD_URL = os.getenv("WAZUH_DASHBOARD_URL", "https://localhost")

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_https_reachable(driver):
    driver.get(DASHBOARD_URL)
    WebDriverWait(driver, 30).until(lambda d: d.title != "")
    assert "Wazuh" in driver.title or driver.title != ""

def test_login_form_present(driver):
    driver.get(DASHBOARD_URL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "username")))
    assert driver.find_element(By.NAME, "username")
    assert driver.find_element(By.NAME, "password")
