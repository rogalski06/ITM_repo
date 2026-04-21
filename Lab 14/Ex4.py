# Create a scatter plot of tips versus fares

import matplotlib.pyplot as plt
import pandas as pd

# Read in the data from the json file
trips_df = pd.read_json('../Trips from area 8.json')

fare_series = trips_df["fare"]
tip_series = trips_df["tips"]

fig = plt.figure()

plt.plot(fare_series, tip_series, marker='.', linestyle='None')
plt.title('Scatterplot of Tips vs Fares')
plt.xlabel('Fares in $')
plt.ylabel('Tips in $')

plt.show()