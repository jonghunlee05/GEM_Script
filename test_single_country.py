import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

def test_uk_electricity():
    """Test United Kingdom electricity values manually"""
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    # Create driver
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to calculator
        print("Navigating to calculator...")
        driver.get("https://terrapass.com/carbon-footprint-calculator/")
        time.sleep(5)
        
        # Switch to iframe
        iframe = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.calculator"))
        )
        driver.switch_to.frame(iframe)
        print("Switched to calculator iframe")
        time.sleep(3)
        
        # Click Individual Calculator
        individual_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Individual Calculator')]"))
        )
        individual_button.click()
        print("Clicked Individual Calculator")
        time.sleep(3)
        
        # Click Home Energy
        home_energy_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'ico-home')]"))
        )
        home_energy_button.click()
        print("Clicked Home Energy")
        time.sleep(3)
        
        # Select United Kingdom
        country_dropdown = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='country']"))
        )
        select = Select(country_dropdown)
        select.select_by_visible_text("United Kingdom")
        print("Selected United Kingdom")
        time.sleep(2)
        
        # Click Next
        next_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
        )
        next_button.click()
        print("Clicked Next")
        time.sleep(3)
        
        # Test different electricity values
        test_values = [50, 100, 250, 500, 1000]
        
        for kwh in test_values:
            print(f"\nTesting {kwh} kWh...")
            
            # Find and enter electricity value
            electricity_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
            )
            electricity_input.clear()
            electricity_input.send_keys(str(kwh))
            print(f"Entered {kwh} kWh")
            
            # Click Next to see results
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
            print("Clicked Next to see results")
            time.sleep(3)
            
            # Take screenshot
            driver.save_screenshot(f"uk_{kwh}kwh_result.png")
            print(f"Screenshot saved as uk_{kwh}kwh_result.png")
            
            # Look for carbon footprint value
            try:
                # Try to find the carbon footprint value
                carbon_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'lbs CO2e')]")
                print(f"Found {len(carbon_elements)} elements containing 'lbs CO2e'")
                for i, elem in enumerate(carbon_elements):
                    text = elem.text
                    print(f"  Element {i+1}: '{text}'")
                    
                    # Try to extract numeric value
                    import re
                    match = re.search(r'(\d+\.?\d*)', text)
                    if match:
                        value = float(match.group(1))
                        print(f"    Extracted value: {value}")
            except Exception as e:
                print(f"Error extracting carbon footprint: {e}")
            
            # Go back to electricity input
            prev_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Prev')]"))
            )
            prev_button.click()
            print("Clicked Prev to go back")
            time.sleep(2)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_uk_electricity() 