from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = FastAPI()

class AccountID(BaseModel):
    account_id: str

@app.post("/get_url/")
def get_url(account: AccountID):
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")  # Applicable to Windows; disable GPU rendering

    # Use WebDriver Manager to handle the ChromeDriver binary
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Navigate to the initial page
        driver.get('https://www.hctax.net/Property/PropertyTax')

        # Enter the account ID
        account_id_input = driver.find_element(By.ID, 'txtSearchValue')
        account_id_input.send_keys(account.account_id)

        # Click the search button
        search_button = driver.find_element(By.ID, 'btnSubmitTaxSearch')
        search_button.click()

        # Wait for the page to load and for the link to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'EncryptAndGo')]")))

        # Click on the link
        link = driver.find_element(By.XPATH, "//a[contains(@onclick, 'EncryptAndGo')]")
        link.click()

        # Wait for the new page to load
        time.sleep(5)

        # Get the current URL
        current_url = driver.current_url
        return {"url": current_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        driver.quit()
