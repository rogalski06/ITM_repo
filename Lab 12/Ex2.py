# Grab 1 month interest rate data from the Treasury website

import pandas as pd
import urllib.request
import lxml

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"

# Get the URL and use read_html to real the data into a DataFrame
print("Opening URL: " + url)
web_page = urllib.request.urlopen(url)
data_frame = pd.read_html(web_page)

# print(data_frame[0].info())
# print(data_frame[0])

# Print the column names to understand the structure of the DataFrame
print("Column names in the DataFrame:")
print(data_frame[0].columns)

# Extract the 1 month interest rate data
one_month_rate = data_frame[0].loc[0, "1 Mo"]
print(f"1 month interest rate on 03/01/2026: {one_month_rate}")