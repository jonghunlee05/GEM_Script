#!/usr/bin/env python3
"""
Test script for the optimized carbon calculator scraper
"""
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from carbon_calculator_scraper import TerrapassCarbonCalculator

def test_optimized_scraper():
    """Test the optimized scraper with a few countries"""
    print("Testing optimized carbon calculator scraper...")
    
    # Create calculator instance
    calculator = TerrapassCarbonCalculator()
    
    # Test with just 3 countries
    test_countries = ["Albania", "Belgium", "Canada"]
    electricity_values = [50, 100]  # Just test 2 values for speed
    
    print(f"Testing {len(test_countries)} countries with {len(electricity_values)} kWh values each...")
    
    try:
        # Setup and navigate
        calculator.setup_driver()
        calculator.navigate_to_calculator()
        
        # Get country list
        countries = calculator.get_country_list()
        if not countries:
            print("Could not get country list")
            return False
            
        # Filter to just our test countries
        test_countries = [c for c in countries if c in test_countries]
        print(f"Found {len(test_countries)} test countries: {test_countries}")
        
        # Test each country
        for country in test_countries:
            print(f"\n--- Testing {country} ---")
            results = calculator.test_country_electricity(country, electricity_values)
            if results:
                calculator.results[country] = results
                print(f"✅ {country}: {results}")
            else:
                print(f"❌ {country}: No results")
                
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    finally:
        calculator.driver.quit()
        
    # Save results
    if calculator.results:
        calculator.save_results("test_results.xlsx")
        print(f"\n✅ Test completed successfully! Results saved to test_results.xlsx")
        print(f"Countries with results: {list(calculator.results.keys())}")
        return True
    else:
        print("\n❌ No results obtained")
        return False

if __name__ == "__main__":
    success = test_optimized_scraper()
    if success:
        print("\n🎉 Optimized scraper is working!")
    else:
        print("\n💥 Optimized scraper has issues") 