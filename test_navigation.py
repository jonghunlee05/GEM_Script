import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_navigation():
    """Test navigation through the calculator steps"""
    
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
        
        # Take screenshot after Individual Calculator
        driver.save_screenshot("after_individual.png")
        print("Screenshot saved as after_individual.png")
        
        # Look for Home Energy button
        home_energy_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'ico-home')]"))
        )
        home_energy_button.click()
        print("Clicked Home Energy button")
        time.sleep(3)
        
        # Take screenshot after Home Energy
        driver.save_screenshot("after_home_energy.png")
        print("Screenshot saved as after_home_energy.png")
        
        # Get page source after Home Energy
        with open("home_energy_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Home energy source saved as home_energy_source.html")
        
        # Look for all elements in home energy section
        print("\nLooking for elements in Home Energy section...")
        
        # Check for country selection
        country_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'COUNTRY') or contains(text(), 'Country')]")
        print(f"Found {len(country_elements)} elements containing 'COUNTRY'")
        for i, elem in enumerate(country_elements):
            print(f"  Country element {i+1}: '{elem.text}' (tag: {elem.tag_name})")
        
        # Check for electricity inputs
        electricity_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'ELECTRICITY') or contains(text(), 'Electricity')]")
        print(f"\nFound {len(electricity_elements)} elements containing 'ELECTRICITY'")
        for i, elem in enumerate(electricity_elements):
            print(f"  Electricity element {i+1}: '{elem.text}' (tag: {elem.tag_name})")
        
        # Check for all inputs
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\nFound {len(inputs)} inputs")
        for i, input_elem in enumerate(inputs):
            print(f"  Input {i+1}: type={input_elem.get_attribute('type')}, placeholder='{input_elem.get_attribute('placeholder')}', name='{input_elem.get_attribute('name')}'")
        
        # Check for all selects
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"\nFound {len(selects)} selects")
        for i, select in enumerate(selects):
            print(f"  Select {i+1}: name='{select.get_attribute('name')}', id='{select.get_attribute('id')}'")
            options = select.find_elements(By.TAG_NAME, "option")
            print(f"    Options ({len(options)}): {[opt.text for opt in options[:5]]}")
        
        # Check for all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"\nFound {len(buttons)} buttons")
        for i, button in enumerate(buttons):
            print(f"  Button {i+1}: '{button.text}' (class: {button.get_attribute('class')})")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_navigation() 