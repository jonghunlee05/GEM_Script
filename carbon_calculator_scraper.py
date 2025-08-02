import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TerrapassCarbonCalculator:
    def __init__(self):
        """Initialize the web driver and setup"""
        self.driver = None
        self.wait = None
        self.results = {}
        self.states_required_countries = []
        self.country_count = 0  # Track countries processed for session management
        
    def random_delay(self, base_delay, variation=0.2):
        """Add random variation to delays to make behavior more human-like"""
        actual_delay = base_delay + random.uniform(-variation, variation)
        actual_delay = max(0.1, actual_delay)  # Minimum 0.1 second
        time.sleep(actual_delay)
        
    def setup_driver(self):
        """Setup Chrome web driver with optimized options"""
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
            # Try to use webdriver-manager to get the correct driver
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error with webdriver-manager: {e}")
            # Fallback to system ChromeDriver
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                print(f"Error with system ChromeDriver: {e2}")
                print("Please make sure Chrome browser is installed and ChromeDriver is available")
                raise
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 5)  # Reduced from 10 to 5 seconds
        
    def navigate_to_calculator(self):
        """Navigate to the Terrapass carbon calculator"""
        url = "https://terrapass.com/carbon-footprint-calculator/"
        self.driver.get(url)
        self.random_delay(2.5)  # Reduced from 5 to 2.5 seconds
        
        # Switch to the calculator iframe
        try:
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.calculator"))
            )
            self.driver.switch_to.frame(iframe)
            print("Switched to calculator iframe")
            self.random_delay(1.5)  # Reduced from 3 to 1.5 seconds
            
            # Select Individual Calculator
            individual_selectors = [
                "//a[contains(text(), 'Individual Calculator')]",  # Prioritize link over button
                "//button[contains(text(), 'Individual Calculator')]",
                "//button[contains(text(), 'Individual')]",
                "//div[contains(text(), 'Individual Calculator')]",
                "//span[contains(text(), 'Individual Calculator')]",
                "//input[@value='Individual Calculator']"
            ]
            
            individual_button = None
            for selector in individual_selectors:
                try:
                    individual_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found Individual Calculator button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if individual_button:
                individual_button.click()
                print("Clicked Individual Calculator button")
                self.random_delay(1.5)  # Reduced from 3 to 1.5 seconds
                
                # Navigate to Home Energy section
                home_energy_selectors = [
                    "//a[contains(@class, 'ico-home')]",
                    "//a[contains(text(), 'Home Energy')]",
                    "//button[contains(text(), 'Home Energy')]",
                    "//div[contains(text(), 'Home Energy')]"
                ]
                
                home_energy_button = None
                for selector in home_energy_selectors:
                    try:
                        home_energy_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"Found Home Energy button with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if home_energy_button:
                    home_energy_button.click()
                    print("Clicked Home Energy button")
                    self.random_delay(1.5)  # Reduced from 3 to 1.5 seconds
                else:
                    print("Could not find Home Energy button")
                    # Continue anyway, maybe we're already in the right section
            else:
                print("Could not find Individual Calculator button")
                # Continue anyway, maybe we're already in the calculator
                
        except TimeoutException:
            print("Could not find calculator iframe")
            raise
        
    def select_country(self, country_name):
        """Select a country from the dropdown"""
        try:
            # Wait for country dropdown to be present - try multiple selectors
            country_selectors = [
                "select[name='country']", 
                "select[id='country']",
                "select[data-name='country']",
                "select",
                "div[role='listbox']",
                "input[placeholder*='country']",
                "input[placeholder*='Country']"
            ]
            
            country_dropdown = None
            for selector in country_selectors:
                try:
                    country_dropdown = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found country dropdown with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not country_dropdown:
                print(f"Could not find country dropdown for {country_name}")
                return False
            
            # Try to select the country
            try:
                select = Select(country_dropdown)
                select.select_by_visible_text(country_name)
                print(f"Selected country: {country_name}")
            except:
                # If it's not a select element, try clicking and typing
                country_dropdown.click()
                self.random_delay(0.5)
                country_dropdown.send_keys(country_name)
                self.random_delay(0.5)
                country_dropdown.send_keys(Keys.ENTER)
            
            self.random_delay(1)  # Reduced from 2 to 1 second
            
            # Check if state/province field appears
            state_selectors = [
                "select[name='state']", 
                "select[id='state']",
                "select[data-name='state']",
                "input[placeholder*='state']",
                "input[placeholder*='State']"
            ]
            
            for selector in state_selectors:
                try:
                    state_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"Country {country_name} requires state selection - skipping")
                    return False
                except NoSuchElementException:
                    continue
            
            print(f"Country {country_name} selected successfully")
            return True
                
        except Exception as e:
            print(f"Error selecting country {country_name}: {e}")
            return False
            
    def click_next(self):
        """Click the NEXT button"""
        try:
            # First, try to handle cookie banner if present
            try:
                cookie_banner = self.driver.find_element(By.ID, "ifrmCookieBanner")
                if cookie_banner.is_displayed():
                    print("Cookie banner detected, switching to it...")
                    self.driver.switch_to.frame(cookie_banner)
                    
                    # Try to find and click accept/close button
                    accept_selectors = [
                        "//button[contains(text(), 'Accept')]",
                        "//button[contains(text(), 'Accept All')]",
                        "//button[contains(text(), 'OK')]",
                        "//button[contains(text(), 'Close')]",
                        "//a[contains(text(), 'Accept')]",
                        "//a[contains(text(), 'Close')]"
                    ]
                    
                    for selector in accept_selectors:
                        try:
                            accept_button = self.driver.find_element(By.XPATH, selector)
                            if accept_button.is_displayed():
                                accept_button.click()
                                print("Clicked cookie banner accept button")
                                break
                        except:
                            continue
                    
                    # Switch back to main content
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, "iframe.calculator"))
                    self.random_delay(0.5)
            except:
                pass  # No cookie banner or already handled
            
            # Try multiple selectors for the NEXT button
            next_selectors = [
                "//button[contains(text(), 'NEXT')]",
                "//button[contains(text(), 'Next')]",
                "//button[contains(text(), 'next')]",
                "//input[@value='NEXT']",
                "//input[@value='Next']",
                "//a[contains(text(), 'NEXT')]",
                "//div[contains(text(), 'NEXT')]",
                "//span[contains(text(), 'NEXT')]"
            ]
            
            next_button = None
            for selector in next_selectors:
                try:
                    next_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found NEXT button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if next_button:
                # Try to scroll the button into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                self.random_delay(0.3)
                
                # Try clicking with JavaScript if regular click fails
                try:
                    next_button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", next_button)
                
                self.random_delay(1)  # Reduced from 2 to 1 second
                return True
            else:
                print("Could not find NEXT button")
                return False
        except Exception as e:
            print(f"Error clicking NEXT button: {e}")
            return False
            
    def input_electricity_consumption(self, kwh_value):
        """Input electricity consumption value"""
        try:
            # Wait for the electricity input section to load
            self.random_delay(1)  # Reduced from 2 to 1 second
            
            # Look for electricity input field - it might be the first input field in the form
            electricity_input = None
            
            # Try to find input by looking for electricity-related text nearby
            electricity_selectors = [
                "//input[preceding-sibling::*[contains(text(), 'ELECTRICITY')]]",
                "//input[following-sibling::*[contains(text(), 'ELECTRICITY')]]",
                "//input[ancestor::*[contains(text(), 'ELECTRICITY')]]",
                "//input[@type='number']",
                "//input[@type='text']",
                "//input"
            ]
            
            for selector in electricity_selectors:
                try:
                    inputs = self.driver.find_elements(By.XPATH, selector)
                    for input_elem in inputs:
                        if input_elem.is_displayed() and input_elem.is_enabled():
                            electricity_input = input_elem
                            print(f"Found electricity input with selector: {selector}")
                            break
                    if electricity_input:
                        break
                except:
                    continue
            
            if not electricity_input:
                print(f"Could not find electricity input field for {kwh_value} kWh")
                return False
            
            # Clear and enter the value
            electricity_input.clear()
            electricity_input.send_keys(str(kwh_value))
            print(f"Entered {kwh_value} kWh")
            
            # Try to ensure kWh and per Month are selected if dropdowns exist
            try:
                unit_dropdowns = self.driver.find_elements(By.CSS_SELECTOR, "select")
                for dropdown in unit_dropdowns:
                    try:
                        select = Select(dropdown)
                        options = [option.text for option in select.options]
                        if "kWh" in options:
                            select.select_by_visible_text("kWh")
                            print("Selected kWh unit")
                        elif "per Month" in options:
                            select.select_by_visible_text("per Month")
                            print("Selected per Month frequency")
                    except:
                        pass
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"Error inputting electricity consumption {kwh_value} kWh: {e}")
            return False
            
    def get_carbon_footprint(self):
        """Extract the carbon footprint value from the dashboard"""
        try:
            # Wait for the carbon dashboard to load
            self.random_delay(1.5)  # Reduced from 3 to 1.5 seconds
            
            # Look for the home energy value in the dashboard
            home_energy_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Home Energy')]/following-sibling::*[contains(text(), 'lbs CO2e')]"))
            )
            
            # Extract the numeric value
            text = home_energy_element.text
            import re
            # Updated regex to handle commas in numbers (e.g., "1,369.07")
            match = re.search(r'([\d,]+\.?\d*)', text)
            if match:
                # Remove commas and convert to float
                value_str = match.group(1).replace(',', '')
                return float(value_str)
            else:
                print("Could not extract carbon footprint value")
                return None
                
        except TimeoutException:
            print("Could not find carbon footprint value")
            return None
            
    def go_back_to_energy_section(self):
        """Go back to the energy input section"""
        try:
            # Try multiple selectors for the PREV button
            prev_selectors = [
                "//button[contains(text(), 'PREV')]",
                "//button[contains(text(), 'Prev')]",
                "//button[contains(text(), 'prev')]",
                "//button[contains(@class, 'btn-prev')]"
            ]
            
            prev_button = None
            for selector in prev_selectors:
                try:
                    prev_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found PREV button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if prev_button:
                prev_button.click()
                self.random_delay(1)  # Reduced from 2 to 1 second
                return True
            else:
                print("Could not find PREV button")
                return False
        except Exception as e:
            print(f"Error going back to energy section: {e}")
            return False
            
    def reset_calculator_state(self):
        """Reset the calculator to the initial country selection state"""
        try:
            # Try to navigate back to the beginning by clicking Prev multiple times
            for i in range(10):  # Try up to 10 times
                try:
                    prev_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Prev')]")
                    if prev_button.is_enabled():
                        prev_button.click()
                        self.random_delay(0.5)  # Reduced from 1 to 0.5 seconds
                    else:
                        break  # No more prev buttons to click
                except:
                    break  # No prev button found
            
            # If we're still not at the beginning, refresh the page
            try:
                country_dropdown = self.driver.find_element(By.CSS_SELECTOR, "select[name='country']")
                # Check if we're at the beginning by looking for the default "Country" option
                select = Select(country_dropdown)
                if select.first_selected_option.text == "Country":
                    print("Successfully reset to country selection state")
                    return True
            except:
                pass
            
            # If we can't reset, refresh the page and re-navigate
            print("Refreshing calculator to reset state...")
            self.driver.refresh()
            self.random_delay(1.5)  # Reduced from 3 to 1.5 seconds
            
            # Re-switch to the iframe (this was missing!)
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.calculator"))
            )
            self.driver.switch_to.frame(iframe)
            self.random_delay(1.5)  # Reduced from 3 to 1.5 seconds
            
            # Re-navigate to Individual Calculator and Home Energy
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
                    individual_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"Found Individual Calculator button with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if individual_button:
                individual_button.click()
                print("Clicked Individual Calculator button")
                time.sleep(3)  # Allow the calculator to load
                
                # Navigate to Home Energy section
                home_energy_selectors = [
                    "//a[contains(@class, 'ico-home')]",
                    "//a[contains(text(), 'Home Energy')]",
                    "//button[contains(text(), 'Home Energy')]",
                    "//div[contains(text(), 'Home Energy')]"
                ]
                
                home_energy_button = None
                for selector in home_energy_selectors:
                    try:
                        home_energy_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        print(f"Found Home Energy button with selector: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if home_energy_button:
                    home_energy_button.click()
                    print("Clicked Home Energy button")
                    time.sleep(3)  # Allow the home energy section to load
                else:
                    print("Could not find Home Energy button")
                    # Continue anyway, maybe we're already in the right section
            else:
                print("Could not find Individual Calculator button")
                # Continue anyway, maybe we're already in the calculator
            
            print("Successfully reset calculator state")
            return True
            
        except Exception as e:
            print(f"Error resetting calculator state: {e}")
            return False
    
    def get_country_list(self):
        """Get the list of countries from the dropdown in alphabetical order"""
        try:
            # Wait a bit longer for the page to fully load
            time.sleep(3)
            
            # Try multiple selectors for the country dropdown
            country_selectors = [
                "select[name='country']",
                "select[id='country']",
                "select[data-name='country']",
                "select"
            ]
            
            country_dropdown = None
            for selector in country_selectors:
                try:
                    country_dropdown = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found country dropdown with selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not country_dropdown:
                print("Could not find country dropdown with any selector")
                return []
            
            select = Select(country_dropdown)
            
            countries = []
            for option in select.options:
                country_name = option.text.strip()
                if country_name and country_name != "Country":  # Skip the default option
                    countries.append(country_name)
            
            print(f"Found {len(countries)} countries in dropdown")
            return countries
            
        except Exception as e:
            print(f"Error getting country list: {e}")
            return []
    
    def test_country_electricity(self, country_name, electricity_values):
        """Test a country with different electricity consumption values"""
        print(f"\nTesting country: {country_name}")
        
        # Try to find country dropdown - if not found, try to navigate back
        try:
            country_dropdown = self.driver.find_element(By.CSS_SELECTOR, "select[name='country']")
        except:
            # If dropdown not found, try to go back multiple times to reach country selection
            print("Country dropdown not found, navigating back to country selection...")
            for attempt in range(5):  # Try up to 5 times
                try:
                    prev_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Prev')]")
                    if prev_button.is_enabled():
                        prev_button.click()
                        self.random_delay(0.3)
                        
                        # Check if we found the dropdown
                        try:
                            country_dropdown = self.driver.find_element(By.CSS_SELECTOR, "select[name='country']")
                            print(f"Found country dropdown after {attempt + 1} back clicks")
                            break
                        except:
                            continue
                    else:
                        print(f"Could not navigate to country selection for {country_name}")
                        return None
                except:
                    print(f"Could not navigate to country selection for {country_name}")
                    return None
            else:
                print(f"Could not find country dropdown after multiple attempts for {country_name}")
                return None
        
        # Select country from dropdown
        try:
            # Wait for country options to load dynamically
            self.random_delay(1)
            
            select = Select(country_dropdown)
            select.select_by_visible_text(country_name)
            print(f"Selected country: {country_name}")
            self.random_delay(1)  # Reduced from 2 to 1 second
        except Exception as e:
            print(f"Error selecting country {country_name}: {e}")
            return None
        
        # Check if state dropdown appears and has options
        try:
            state_dropdown = self.driver.find_element(By.CSS_SELECTOR, "select[name='state']")
            state_options = state_dropdown.find_elements(By.TAG_NAME, "option")
            if len(state_options) > 1:  # More than just "State"
                print(f"Country {country_name} requires state selection - adding to states_required list")
                self.states_required_countries.append(country_name)
                return None
        except:
            pass  # No state dropdown, continue
            
        # Click NEXT to proceed to electricity input section
        if not self.click_next():
            return None
            
        country_results = {}
        
        # Batch test all kWh values for this country
        for kwh in electricity_values:
            print(f"  Testing {kwh} kWh...")
            
            # Input electricity consumption
            if not self.input_electricity_consumption(kwh):
                continue
                
            # Click NEXT to see results
            if not self.click_next():
                continue
                
            # Get carbon footprint
            carbon_value = self.get_carbon_footprint()
            if carbon_value is not None:
                country_results[kwh] = carbon_value
                print(f"    Result: {carbon_value} lbs CO2e")
                
            # Go back to energy section for next test
            if not self.go_back_to_energy_section():
                break
                
        return country_results
        
    def run_analysis(self, electricity_values):
        """Run the complete analysis with session management and error handling"""
        self.setup_driver()
        
        try:
            self.navigate_to_calculator()
            
            # Get the actual country list from the dropdown
            countries = self.get_country_list()
            if not countries:
                print("Could not get country list from dropdown")
                return
            
            print(f"Testing {len(countries)} countries in alphabetical order...")
            
            for i, country in enumerate(countries):
                try:
                    print(f"\n--- Processing country {i+1}/{len(countries)}: {country} ---")
                    
                    results = self.test_country_electricity(country, electricity_values)
                    if results:
                        self.results[country] = results
                    
                    # Session management: restart browser every 50 countries
                    self.country_count += 1
                    if self.country_count % 50 == 0:
                        print(f"\n--- Restarting browser after {self.country_count} countries ---")
                        self.driver.quit()
                        self.random_delay(2)  # Brief pause
                        self.setup_driver()
                        self.navigate_to_calculator()
                    
                    # Save intermediate results every 10 countries
                    if self.country_count % 10 == 0:
                        self.save_results("intermediate_results.xlsx")
                        print(f"Saved intermediate results after {self.country_count} countries")
                        
                except Exception as e:
                    print(f"Error processing country {country}: {e}")
                    # Try to recover by restarting the driver
                    try:
                        print("Attempting driver recovery...")
                        self.driver.quit()
                        self.random_delay(2)
                        self.setup_driver()
                        self.navigate_to_calculator()
                    except Exception as recovery_error:
                        print(f"Failed to recover driver: {recovery_error}")
                        break
                    
        finally:
            self.driver.quit()
            
    def save_results(self, filename="carbon_footprint_results.xlsx"):
        """Save results to Excel file"""
        if not self.results:
            print("No results to save")
            return
            
        # Create DataFrame
        data = []
        electricity_values = [50, 100, 250, 500, 1000]
        
        for country, results in self.results.items():
            row = {'Country': country}
            for kwh in electricity_values:
                row[f'{kwh}kwh'] = results.get(kwh, 'N/A')
            data.append(row)
            
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Results saved to {filename}")
        
        # Also save as CSV
        csv_filename = filename.replace('.xlsx', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"Results also saved to {csv_filename}")

def main():
    """Main function to run the analysis"""
    # Electricity consumption values to test
    electricity_values = [50, 100, 250, 500, 1000]
    
    # Create calculator instance
    calculator = TerrapassCarbonCalculator()
    
    # Run the analysis
    print("Starting Terrapass Carbon Calculator Analysis...")
    calculator.run_analysis(electricity_values)
    
    # Save results
    calculator.save_results()
    
    # Print summary
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    
    print(f"\nCountries with results: {len(calculator.results)}")
    print(f"Countries requiring state selection: {len(calculator.states_required_countries)}")
    
    print(f"\nCountries requiring state selection:")
    for country in calculator.states_required_countries:
        print(f"  - {country}")
    
    print(f"\nCountries with carbon footprint results:")
    for country, results in calculator.results.items():
        print(f"\n{country}:")
        for kwh, carbon in results.items():
            print(f"  {kwh} kWh: {carbon} lbs CO2e")
    
    # Save states required countries to a separate file
    if calculator.states_required_countries:
        with open("states_required_countries.txt", "w") as f:
            for country in calculator.states_required_countries:
                f.write(f"{country}\n")
        print(f"\nStates required countries saved to: states_required_countries.txt")

if __name__ == "__main__":
    main() 