# Create a headmap from pickup_community_area and dropoff_community_area based on “taxi trips Fri 7_7_2017.csv”.

# Import the necessary libraries
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

# Read in the data from the CSV file
trips_df = pd.read_csv("../taxi trips Fri 7_7_2017.csv")

# Create a heatmap of pickup and dropoff community areas
heatmap_data = trips_df.pivot_table(index='pickup_community_area', columns='dropoff_community_area', aggfunc='size', fill_value=0)
plt.figure(figsize=(10, 8))

# Create the heatmap using seaborn
sns.heatmap(heatmap_data, cmap='YlGnBu', fmt='d', linewidths=.5)

# Set the title and labels for the plot
plt.title("Heatmap of Pickup and Dropoff Community Areas")
plt.xlabel("Dropoff Community Area")
plt.ylabel("Pickup Community Area")
plt.savefig("Heatmap of Pickup and Dropoff Community Areas.png", dpi=300)

plt.show()