# Create a chart of tips by payment type

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read in the data from the json file
trips_df = pd.read_json('../Trips from area 8.json')

# Extract the tips and payment type data
trips_df = trips_df[['tips', 'payment_type']]
fig = plt.figure()

# Drop rows with NA values
trips_df = trips_df.dropna()
trips_df = trips_df.astype({'tips': 'float'})
trips_df = trips_df.set_index('payment_type')

# Sum the tips by payment type
tips_by_payment = trips_df.groupby('payment_type')['tips'].sum()

x_labels = pd.Series(tips_by_payment.index.values)
y_values = pd.Series(tips_by_payment["tips"].values)

bars = np.array(range(len(x_labels)))
plt.xticks(bars, x_labels, color='red', fontweight='bold')

# Create the bar chart of tips by payment type
plt.bar(bars, y_values)
plt.xlabel('Payment Type')
plt.ylabel('Total Tips in $')
plt.title('Tips by Payment Type')

plt.show()