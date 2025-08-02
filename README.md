# Terrapass Carbon Calculator Scraper

This script automates the Terrapass carbon footprint calculator to collect data on how different countries calculate carbon emissions for electricity consumption.

## Features

- Automatically tests different electricity consumption values (50, 100, 250, 500, 1000 kWh per month)
- Handles multiple countries
- Skips countries that require additional location fields (state/province)
- Exports results to both Excel (.xlsx) and CSV formats
- Provides real-time progress updates

## Requirements

- Python 3.7+
- Chrome browser installed
- Internet connection

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The script will automatically download and manage the Chrome WebDriver.

## Usage

Run the script:
```bash
python carbon_calculator_scraper.py
```

## Output

The script will create two files:
- `carbon_footprint_results.xlsx` - Excel file with results
- `carbon_footprint_results.csv` - CSV file with results

The output format will be:
| Country | 50kwh | 100kwh | 250kwh | 500kwh | 1000kwh |
|---------|-------|--------|--------|--------|---------|
| United States | 123.45 | 246.90 | 617.25 | 1234.50 | 2469.00 |

## How it Works

1. **Country Selection**: The script selects a country from the dropdown
2. **Location Check**: If the country requires state/province selection, it skips that country
3. **Energy Input**: For valid countries, it proceeds to the energy section
4. **Testing**: For each electricity value (50, 100, 250, 500, 1000 kWh), it:
   - Enters the value
   - Clicks NEXT to see results
   - Extracts the carbon footprint value
   - Goes back to test the next value
5. **Data Export**: Results are saved to Excel and CSV files

## Current Test Countries

- United States
- Canada  
- United Kingdom

## Notes

- The script includes delays to handle page loading and avoid being detected as a bot
- Countries that require additional location fields are automatically skipped
- The script will print progress updates as it runs
- If any step fails, the script will continue with the next test case

## Troubleshooting

If you encounter issues:

1. **Chrome not found**: Make sure Chrome browser is installed
2. **WebDriver issues**: The script automatically downloads the correct WebDriver version
3. **Page loading issues**: The script includes timeouts and retry logic
4. **Element not found**: The website structure may have changed - check the selectors in the code

## Customization

To test different countries or electricity values, modify the `main()` function in the script:

```python
# Change test countries
test_countries = ["Germany", "France", "Australia"]

# Change electricity values
electricity_values = [25, 75, 150, 300, 750]
``` 