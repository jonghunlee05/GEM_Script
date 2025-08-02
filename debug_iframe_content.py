import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def debug_iframe_content():
    """Debug script to inspect the iframe content after selecting Individual Calculator"""
    
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
        
        # Take screenshot of initial iframe content
        driver.save_screenshot("iframe_initial.png")
        print("Screenshot saved as iframe_initial.png")
        
        # Look for Individual Calculator button
        individual_selectors = [
            "//button[contains(text(), 'Individual Calculator')]",
            "//button[contains(text(), 'Individual')]",
            "//div[contains(text(), 'Individual Calculator')]",
            "//span[contains(text(), 'Individual Calculator')]",
            "//a[contains(text(), 'Individual Calculator')]",
            "//input[@value='Individual Calculator']"
        ]
        
        individual_button = None
        for selector in individual_selectors:
            try:
                individual_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"Found Individual Calculator button with selector: {selector}")
                break
            except:
                continue
        
        if individual_button:
            individual_button.click()
            print("Clicked Individual Calculator button")
            time.sleep(5)  # Allow calculator to load
            
            # Take screenshot after clicking Individual Calculator
            driver.save_screenshot("iframe_after_individual.png")
            print("Screenshot saved as iframe_after_individual.png")
            
            # Get page source of iframe content
            with open("iframe_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Iframe source saved as iframe_source.html")
            
            # Look for all elements
            print("\nLooking for all elements in iframe...")
            
            # Buttons
            buttons = driver.find_elements(By.TAG_NAME, "button")
            print(f"Found {len(buttons)} buttons")
            for i, button in enumerate(buttons[:10]):
                print(f"  Button {i+1}: '{button.text}' (class: {button.get_attribute('class')})")
            
            # Inputs
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"\nFound {len(inputs)} inputs")
            for i, input_elem in enumerate(inputs[:10]):
                print(f"  Input {i+1}: type={input_elem.get_attribute('type')}, placeholder='{input_elem.get_attribute('placeholder')}', name='{input_elem.get_attribute('name')}'")
            
            # Selects
            selects = driver.find_elements(By.TAG_NAME, "select")
            print(f"\nFound {len(selects)} selects")
            for i, select in enumerate(selects):
                print(f"  Select {i+1}: name='{select.get_attribute('name')}', id='{select.get_attribute('id')}'")
                options = select.find_elements(By.TAG_NAME, "option")
                print(f"    Options ({len(options)}): {[opt.text for opt in options[:5]]}")
            
            # Divs with text
            divs = driver.find_elements(By.TAG_NAME, "div")
            print(f"\nFound {len(divs)} divs")
            for i, div in enumerate(divs[:20]):
                text = div.text.strip()
                if text:
                    print(f"  Div {i+1}: '{text[:50]}...' (class: {div.get_attribute('class')})")
            
        else:
            print("Could not find Individual Calculator button")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_iframe_content() 