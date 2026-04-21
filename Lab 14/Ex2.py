# Create a histogram from the trip miles data

import matplotlib.pyplot as plt
import pandas as pd

# Read in the data from the json file
trips_df = pd.read_json('../Trips from area 8.json')

# Extract the trip miles data
trip_miles_series = trips_df['trip_miles']

fig = plt.figure()

# Create the histogram of trip miles data
plt.hist(trip_miles_series)
plt.xlabel('Trip Miles')
plt.ylabel('Frequency')
plt.title('Distribution of Taxi Trip Miles')

plt.show()