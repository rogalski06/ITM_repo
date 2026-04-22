# Create a 3D plot of fares, trip miles and dropoff area based on “Trips from area 8.json”. To do this you will need to add this line to your code: 

# Import the necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

# Read in the data from the JSON file
trips_df = pd.read_json("../Trips from area 8.json")

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract the relevant data for the plot
fare_series = trips_df["fare"]
miles_series = trips_df["trip_miles"]
dropoff_series = trips_df["dropoff_community_area"]

# Plot the data
ax.scatter(miles_series, fare_series, dropoff_series, marker='o', alpha=0.5)
ax.set_title("Fares, Trip Miles and Dropoff Area")
ax.set_xlabel("Trip Miles")
ax.set_ylabel("Fares in $")
ax.set_zlabel("Dropoff Area")
plt.savefig("Fares, Trip Miles and Dropoff Area.png", dpi=300)

plt.show()