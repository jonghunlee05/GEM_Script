#!/usr/bin/env python3
"""
Multi-Tab Smart Business Carbon Calculator Scraper
Distributes countries across 5 tabs, each using smart input modification
"""
import time
import random
import pandas as pd
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MultiTabSmartBusinessScraper:
    def __init__(self):
        """Initialize the multi-tab smart business scraper"""
        self.results = {}  # Shared results dictionary
        self.states_required_countries = []
        self.lock = threading.Lock()  # Thread safety for shared data
        
    def random_delay(self, base_delay, variation=0.2):
        """Add random variation to delays"""
        actual_delay = base_delay + random.uniform(-variation, variation)
        actual_delay = max(0.1, actual_delay)
        time.sleep(actual_delay)
        
    def setup_driver(self, tab_id):
        """Setup Chrome web driver for a specific tab"""
        chrome_options = webdriver.ChromeOptions()
        
        # Headless mode for faster performance
        chrome_options.add_argument("--headless")
        
        # Performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional performance optimizations
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=4096")
        
        # Set Chrome binary path for macOS
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Error with ChromeDriver: {e}")
            raise
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        wait = WebDriverWait(driver, 5)
        
        return driver, wait
        
    def navigate_to_calculator(self, driver, wait):
        """Navigate to the Terrapass carbon calculator"""
        url = "https://terrapass.com/carbon-footprint-calculator/"
        driver.get(url)
        self.random_delay(2.5)
        
        # Switch to the calculator iframe
        try:
            iframe = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.calculator"))
            )
            driver.switch_to.frame(iframe)
            self.random_delay(1.5)
            
            # Select Business Calculator
            business_selectors = [
                "//a[contains(text(), 'Business Calculator')]",
                "//button[contains(text(), 'Business Calculator')]"
            ]
            
            business_button = None
            for selector in business_selectors:
                try:
                    business_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if business_button:
                business_button.click()
                self.random_delay(1.5)
                
                # Business Calculator automatically goes to Business Site page (SITE type is default)
                # No additional navigation needed
                    
        except TimeoutException:
            print("Could not find calculator iframe")
            raise
            
    def handle_cookie_banner(self, driver):
        """Handle cookie banner if present"""
        try:
            cookie_banner = driver.find_element(By.ID, "ifrmCookieBanner")
            if cookie_banner.is_displayed():
                driver.switch_to.frame(cookie_banner)
                
                accept_selectors = [
                    "//button[contains(text(), 'Accept')]",
                    "//button[contains(text(), 'Accept All')]",
                    "//button[contains(text(), 'OK')]",
                    "//button[contains(text(), 'Close')]"
                ]
                
                for selector in accept_selectors:
                    try:
                        accept_button = driver.find_element(By.XPATH, selector)
                        if accept_button.is_displayed():
                            accept_button.click()
                            break
                    except:
                        continue
                
                driver.switch_to.default_content()
                driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe.calculator"))
                self.random_delay(0.5)
        except:
            pass
            
    def click_next(self, driver, wait):
        """Click the NEXT button"""
        try:
            # Handle cookie banner first
            self.handle_cookie_banner(driver)
            
            next_selectors = [
                "//button[contains(text(), 'NEXT')]",
                "//button[contains(text(), 'Next')]",
                "//button[contains(text(), 'next')]"
            ]
            
            next_button = None
            for selector in next_selectors:
                try:
                    next_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if next_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                self.random_delay(0.3)
                
                try:
                    next_button.click()
                except:
                    driver.execute_script("arguments[0].click();", next_button)
                
                self.random_delay(1)
                return True
            else:
                return False
        except Exception as e:
            return False
            
    def get_carbon_footprint(self, driver, wait):
        """Extract the carbon footprint value"""
        try:
            self.random_delay(1.5)
            
            # Try multiple selectors for business calculator results
            result_selectors = [
                "//*[contains(text(), 'Business Site')]/following-sibling::*[contains(text(), 'lbs CO2e')]",
                "//*[contains(text(), 'lbs CO2e')]",
                "//*[contains(text(), 'CO2e')]",
                "//*[contains(text(), 'carbon')]",
                "//*[contains(text(), 'footprint')]"
            ]
            
            for selector in result_selectors:
                try:
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    text = element.text
                    import re
                    match = re.search(r'([\d,]+\.?\d*)', text)
                    if match:
                        value_str = match.group(1).replace(',', '')
                        return float(value_str)
                except TimeoutException:
                    continue
                except Exception as e:
                    continue
            
            return None
                
        except Exception as e:
            return None
            
    def find_electricity_input(self, driver):
        """Find the electricity input field"""
        try:
            electricity_selectors = [
                "//input[@type='text']",
                "//input[@type='number']",
                "//input"
            ]
            
            for selector in electricity_selectors:
                try:
                    inputs = driver.find_elements(By.XPATH, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.is_enabled():
                            return input_elem
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"Error finding electricity input: {e}")
            return None
            
    def modify_electricity_input(self, driver, kwh_value):
        """Modify the electricity input value directly using JavaScript"""
        try:
            # Always find the input field fresh to avoid stale element issues
            electricity_input = self.find_electricity_input(driver)
            if not electricity_input:
                return False
            
            # Clear and set new value using JavaScript
            driver.execute_script("arguments[0].value = '';", electricity_input)
            driver.execute_script(f"arguments[0].value = '{kwh_value}';", electricity_input)
            
            # Trigger change events
            driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, electricity_input)
            
            self.random_delay(0.5)
            return True
            
        except Exception as e:
            print(f"Error modifying electricity input: {e}")
            return False
            
    def test_country_all_kwh(self, country_name, electricity_values, driver, wait, tab_id):
        """Test a country with all kWh values using smart input modification"""
        print(f"[Tab {tab_id}] Testing country: {country_name}")
        
        # Try to find country dropdown
        try:
            country_dropdown = driver.find_element(By.CSS_SELECTOR, "select[name='country']")
        except:
            # Navigate back to country selection
            print(f"[Tab {tab_id}] Navigating back to country selection...")
            for attempt in range(3):
                try:
                    prev_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Prev')]")
                    if prev_button.is_enabled():
                        prev_button.click()
                        self.random_delay(0.3)
                        
                        try:
                            country_dropdown = driver.find_element(By.CSS_SELECTOR, "select[name='country']")
                            break
                        except:
                            continue
                    else:
                        return None
                except:
                    return None
            else:
                return None
        
        # Select country
        try:
            self.random_delay(1)
            select = Select(country_dropdown)
            
            # Debug: Print available options
            available_options = [option.text for option in select.options]
            if country_name not in available_options:
                print(f"[Tab {tab_id}] Country '{country_name}' not found in dropdown. Available options: {available_options[:5]}...")
                return None
            
            select.select_by_visible_text(country_name)
            self.random_delay(1)
            print(f"[Tab {tab_id}] Successfully selected {country_name}")
        except Exception as e:
            print(f"[Tab {tab_id}] Error selecting country {country_name}: {e}")
            return None
        
        # Check for state requirement
        try:
            state_dropdown = driver.find_element(By.CSS_SELECTOR, "select[name='state']")
            state_options = state_dropdown.find_elements(By.TAG_NAME, "option")
            if len(state_options) > 1:
                print(f"[Tab {tab_id}] Country {country_name} requires state selection")
                with self.lock:
                    if country_name not in self.states_required_countries:
                        self.states_required_countries.append(country_name)
                return None
        except:
            pass
            
        # Click NEXT to electricity input (only once)
        if not self.click_next(driver, wait):
            return None
            
        country_results = {}
        
        # Test all kWh values using smart input modification
        for kwh in electricity_values:
            print(f"[Tab {tab_id}]   Testing {kwh} kWh...")
            
            # Modify input value directly
            if not self.modify_electricity_input(driver, kwh):
                continue
                
            # Click NEXT to see results
            if not self.click_next(driver, wait):
                continue
                
            # Get carbon footprint
            carbon_value = self.get_carbon_footprint(driver, wait)
            if carbon_value is not None:
                country_results[kwh] = carbon_value
                print(f"[Tab {tab_id}]     Result: {carbon_value} lbs CO2e")
            else:
                print(f"[Tab {tab_id}]     No result found - trying to debug...")
                # Debug: Print page source to see what's available
                try:
                    page_source = driver.page_source
                    if "lbs CO2e" in page_source:
                        print(f"[Tab {tab_id}]     Page contains 'lbs CO2e' text")
                    if "CO2e" in page_source:
                        print(f"[Tab {tab_id}]     Page contains 'CO2e' text")
                    if "Business Site" in page_source:
                        print(f"[Tab {tab_id}]     Page contains 'Business Site' text")
                except:
                    pass
                
            # Go back to energy section for next test
            try:
                prev_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Prev')]")
                if prev_button.is_enabled():
                    prev_button.click()
                    self.random_delay(0.5)
            except:
                break
                
        return country_results
        
    def worker_tab(self, countries, electricity_values, tab_id):
        """Worker function for each tab"""
        print(f"[Tab {tab_id}] Starting worker with {len(countries)} countries...")
        
        driver, wait = self.setup_driver(tab_id)
        tab_results = {}
        
        try:
            self.navigate_to_calculator(driver, wait)
            
            for i, country in enumerate(countries):
                try:
                    print(f"[Tab {tab_id}] Processing {i+1}/{len(countries)}: {country}")
                    
                    results = self.test_country_all_kwh(country, electricity_values, driver, wait, tab_id)
                    if results:
                        tab_results[country] = results
                        
                        # Save tab results thread-safely
                        with self.lock:
                            self.results[country] = results
                    
                    # Save intermediate results every 2 countries (more frequent for 20 tabs)
                    if (i + 1) % 2 == 0:
                        self.save_tab_results(tab_results, f"intermediate_business_tab{tab_id}_{i+1}.xlsx")
                        print(f"[Tab {tab_id}] Saved intermediate results after {i+1} countries")
                        
                except Exception as e:
                    print(f"[Tab {tab_id}] Error processing {country}: {e}")
                    continue
                    
        finally:
            driver.quit()
            
        # Save final tab results
        self.save_tab_results(tab_results, f"final_business_tab{tab_id}.xlsx")
        print(f"[Tab {tab_id}] Completed! Processed {len(tab_results)} countries")
            
    def save_tab_results(self, tab_results, filename):
        """Save tab results to Excel file"""
        if not tab_results:
            return
            
        # Create DataFrame
        data = []
        electricity_values = [1000, 5000, 10000, 25000, 50000, 100000]
        
        for country, results in tab_results.items():
            row = {'Country': country}
            for kwh in electricity_values:
                row[f'{kwh}kwh'] = results.get(kwh, 'N/A')
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Tab results saved to {filename}")
        
    def run_multi_tab_smart_analysis(self, electricity_values):
        """Run the multi-tab smart analysis"""
        print("Starting Multi-Tab Smart Business Carbon Calculator Analysis...")
        
        # Get country list first
        temp_driver, temp_wait = self.setup_driver(0)
        try:
            self.navigate_to_calculator(temp_driver, temp_wait)
            
            # Get country list
            try:
                country_dropdown = temp_wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='country']"))
                )
                select = Select(country_dropdown)
                all_countries = [option.text for option in select.options if option.text != "Country"]
                print(f"Found {len(all_countries)} countries")
                
                if len(all_countries) == 0:
                    print("ERROR: No countries found in dropdown. Trying alternative approach...")
                    # Try to get page source to debug
                    page_source = temp_driver.page_source
                    if "select" in page_source:
                        print("Page contains select elements")
                    if "country" in page_source:
                        print("Page contains 'country' text")
                    raise Exception("No countries found in dropdown")
                    
            except Exception as e:
                print(f"Error getting country list: {e}")
                # Use a fallback list of countries for testing
                all_countries = ["United States", "Albania", "Angola", "Argentina"]
                print(f"Using fallback list: {all_countries}")
            
        finally:
            temp_driver.quit()
            
        # For testing: Use only 2 tabs with 2 countries each
        test_countries = all_countries[:4]  # Take first 4 countries for testing
        tab_countries = [
            test_countries[:2],  # First 2 countries for tab 1
            test_countries[2:]   # Last 2 countries for tab 2
        ]
            
        print("Country distribution for testing:")
        for i, countries in enumerate(tab_countries):
            print(f"Tab {i+1}: {len(countries)} countries ({countries[0]} to {countries[-1]})")
            
        # Create threads for each tab
        threads = []
        for i, countries in enumerate(tab_countries):
            thread = threading.Thread(
                target=self.worker_tab,
                args=(countries, electricity_values, i+1)
            )
            threads.append(thread)
            
        # Start all threads with staggered timing
        for i, thread in enumerate(threads):
            thread.start()
            self.random_delay(0.5)  # Slower stagger for testing
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        print("All tabs completed!")
        
    def save_final_results(self, filename="multi_tab_smart_business_results.xlsx"):
        """Save final merged results to Excel file"""
        if not self.results:
            print("No results to save")
            return
            
        # Create DataFrame
        data = []
        electricity_values = [1000, 5000, 10000, 25000, 50000, 100000]
        
        for country, results in self.results.items():
            row = {'Country': country}
            for kwh in electricity_values:
                row[f'{kwh}kwh'] = results.get(kwh, 'N/A')
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Final results saved to {filename}")
        
        # Also save as CSV
        csv_filename = filename.replace('.xlsx', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"Final results also saved to {csv_filename}")

def main():
    """Main function to run the multi-tab smart business analysis"""
    electricity_values = [1000, 5000, 10000, 25000, 50000, 100000]
    
    scraper = MultiTabSmartBusinessScraper()
    
    # Run the multi-tab smart analysis
    scraper.run_multi_tab_smart_analysis(electricity_values)
    
    # Save final results
    scraper.save_final_results()
    
    # Print summary
    print("\n" + "="*50)
    print("MULTI-TAB SMART BUSINESS ANALYSIS SUMMARY")
    print("="*50)
    
    print(f"\nCountries with results: {len(scraper.results)}")
    print(f"Countries requiring state selection: {len(scraper.states_required_countries)}")
    
    if scraper.states_required_countries:
        print(f"\nCountries requiring state selection:")
        for country in scraper.states_required_countries:
            print(f"  - {country}")
    
    # Save states required countries
    if scraper.states_required_countries:
        with open("states_required_countries_multi_tab_smart_business.txt", "w") as f:
            for country in scraper.states_required_countries:
                f.write(f"{country}\n")
        print(f"\nStates required countries saved to: states_required_countries_multi_tab_smart_business.txt")

if __name__ == "__main__":
    main() 