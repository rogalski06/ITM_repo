# Scrape data from the City of Chicigo's Data Portal
# Print any line that has a <title> tag in it

import urllib.request

url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

print("Opening URL: " + url)
web_page = urllib.request.urlopen(url)

# Iterate through each line in the web page, searching for the title tag
for line in web_page:
    line = line.decode("utf-8") # Convert the line from bytes to a string
    if "<title>" in line:
        print(line.strip()) # Print the line, removing any leading/trailing whitespace