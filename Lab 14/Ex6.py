# Create a scatter plot of fares by trip miles based on “Trips from area 8.json”.
# Save the plot to a file called FaresXmiles.png
# Filter out trips of 0 miles.
# Filter out trips less than 2 miles.
# What anomalies do you notice in the data?

# Import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd

# Read in the data from the JSON file
trips_df = pd.read_json("../Trips from area 8.json")

# Filter out trips of 0 miles
trips_df = trips_df[trips_df["trip_miles"] > 0]

# Filter out trips less than 2 miles
trips_df = trips_df[trips_df["trip_miles"] > 2]

# Create the scatter plot
fare_series = trips_df["fare"]
miles_series = trips_df["trip_miles"]
fig = plt.figure()

# Plot the data
plt.plot(miles_series, fare_series, linestyle='none', marker='.')
plt.title("Fares by Taxi Trip Miles")
plt.xlabel("Trip Miles")
plt.ylabel("Fares in $")
plt.savefig("Fares by Trip Miles.png", dpi=300)

plt.show()