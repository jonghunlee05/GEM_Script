import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def debug_calculator():
    """Debug script to inspect the Terrapass calculator page"""
    
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
        
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Take screenshot
        driver.save_screenshot("calculator_page.png")
        print("Screenshot saved as calculator_page.png")
        
        # Look for all select elements
        print("\nLooking for select elements...")
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"Found {len(selects)} select elements")
        
        for i, select in enumerate(selects):
            try:
                print(f"\nSelect {i+1}:")
                print(f"  ID: {select.get_attribute('id')}")
                print(f"  Name: {select.get_attribute('name')}")
                print(f"  Class: {select.get_attribute('class')}")
                
                # Get options
                options = select.find_elements(By.TAG_NAME, "option")
                print(f"  Options ({len(options)}):")
                for j, option in enumerate(options[:5]):  # Show first 5 options
                    print(f"    {j+1}. {option.text}")
                if len(options) > 5:
                    print(f"    ... and {len(options)-5} more")
                    
            except Exception as e:
                print(f"  Error: {e}")
        
        # Look for all input elements
        print("\nLooking for input elements...")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(inputs)} input elements")
        
        for i, input_elem in enumerate(inputs[:10]):  # Show first 10 inputs
            try:
                print(f"\nInput {i+1}:")
                print(f"  Type: {input_elem.get_attribute('type')}")
                print(f"  ID: {input_elem.get_attribute('id')}")
                print(f"  Name: {input_elem.get_attribute('name')}")
                print(f"  Placeholder: {input_elem.get_attribute('placeholder')}")
                print(f"  Class: {input_elem.get_attribute('class')}")
            except Exception as e:
                print(f"  Error: {e}")
        
        # Look for buttons
        print("\nLooking for buttons...")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(buttons)} buttons")
        
        for i, button in enumerate(buttons[:10]):  # Show first 10 buttons
            try:
                print(f"\nButton {i+1}:")
                print(f"  Text: {button.text}")
                print(f"  ID: {button.get_attribute('id')}")
                print(f"  Class: {button.get_attribute('class')}")
            except Exception as e:
                print(f"  Error: {e}")
        
        # Look for any elements containing "country"
        print("\nLooking for elements containing 'country'...")
        country_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'COUNTRY', 'country'), 'country') or contains(@id, 'country') or contains(@name, 'country') or contains(@class, 'country')]")
        print(f"Found {len(country_elements)} elements containing 'country'")
        
        for i, elem in enumerate(country_elements):
            try:
                print(f"\nCountry element {i+1}:")
                print(f"  Tag: {elem.tag_name}")
                print(f"  Text: {elem.text}")
                print(f"  ID: {elem.get_attribute('id')}")
                print(f"  Name: {elem.get_attribute('name')}")
                print(f"  Class: {elem.get_attribute('class')}")
            except Exception as e:
                print(f"  Error: {e}")
        
        # Get page source for manual inspection
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("\nPage source saved as page_source.html")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_calculator() 