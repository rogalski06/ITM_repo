# Use the requests package to retrieve a page of mortgage rate info from the Hawaii Board of Realtors site that lists current local mortgage rates: https://www.hicentral.com/hawaii-mortgage-rates.php 
# a. Find the rate table and extract each row.
# b. Output the name of each bank and its current rates per row.

# Import relevant libraries
import requests
from bs4 import BeautifulSoup
import re

# Define the URL for the Hawaii Board of Realtors mortgage rates page
hbr_url = "https://www.hicentral.com/hawaii-mortgage-rates.php"

# Retrieve the HTML content of the page
hbr_html = requests.get(hbr_url).text
html_to_parse = BeautifulSoup(hbr_html, "html.parser")

# print(html_to_parse.prettify())

# Find and print the mortgage rate table and extract each row
mortgage_table = html_to_parse.find("table")
table_rows = mortgage_table.find_all("tr")

# Initialize a variable to keep track of the current bank name
current_bank = None

# Loop through the table rows and extract the bank name and its current rates and print
for row in table_rows[1:]:  # skip header
    cells = row.find_all("td") # find cells within each row
    if cells:
        if cells[0].get_text(strip=True):
            bank_text = cells[0].get_text(strip=True)
            current_bank = re.sub(r'\d{3}-\d{3}-\d{4}', '', bank_text) # replace phone numbers with empty strings by recognizing the digit pattern
            current_bank = re.sub(r'NMLS#\d+', '', current_bank).strip() # strip the NMLS numbers and any blank spaces
        term = cells[1].get_text(strip=True) if len(cells) > 1 else ''
        rate = cells[2].get_text(strip=True) if len(cells) > 2 else ''
        points = cells[3].get_text(strip=True) if len(cells) > 3 else ''
        apr = cells[4].get_text(strip=True) if len(cells) > 4 else ''
        if current_bank and term:
            print(f"\n{current_bank}:\n{term} - Rate: {rate}, Points: {points}, APR: {apr}")