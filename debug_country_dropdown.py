import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def debug_country_dropdown():
    """Debug script to check what elements are available after Home Energy navigation"""
    
    # Setup driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error with ChromeDriver: {e}")
        return
    
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to calculator
        url = "https://terrapass.com/carbon-footprint-calculator/"
        driver.get(url)
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
        time.sleep(5)  # Wait longer for the page to load
        
        # Take screenshot
        driver.save_screenshot("debug_home_energy.png")
        print("Saved screenshot: debug_home_energy.png")
        
        # Save page source
        with open("debug_home_energy_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Saved page source: debug_home_energy_source.html")
        
        # Look for all select elements
        select_elements = driver.find_elements(By.TAG_NAME, "select")
        print(f"\nFound {len(select_elements)} select elements:")
        for i, select in enumerate(select_elements):
            try:
                name = select.get_attribute("name") or "no-name"
                id_attr = select.get_attribute("id") or "no-id"
                print(f"  {i+1}. name='{name}', id='{id_attr}'")
                
                # Try to get options
                select_obj = Select(select)
                options = [opt.text for opt in select_obj.options]
                print(f"     Options: {options[:5]}...")  # Show first 5 options
            except Exception as e:
                print(f"     Error reading select: {e}")
        
        # Look for all input elements
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        print(f"\nFound {len(input_elements)} input elements:")
        for i, input_elem in enumerate(input_elements[:10]):  # Show first 10
            try:
                name = input_elem.get_attribute("name") or "no-name"
                placeholder = input_elem.get_attribute("placeholder") or "no-placeholder"
                type_attr = input_elem.get_attribute("type") or "no-type"
                print(f"  {i+1}. name='{name}', placeholder='{placeholder}', type='{type_attr}'")
            except Exception as e:
                print(f"     Error reading input: {e}")
        
        # Look for elements containing "country" or "Country"
        country_elements = driver.find_elements(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'country')]")
        print(f"\nFound {len(country_elements)} elements containing 'country':")
        for i, elem in enumerate(country_elements[:5]):  # Show first 5
            try:
                tag = elem.tag_name
                text = elem.text[:50] if elem.text else "no-text"
                print(f"  {i+1}. <{tag}> {text}...")
            except Exception as e:
                print(f"     Error reading element: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_country_dropdown() 