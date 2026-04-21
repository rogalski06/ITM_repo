# Visualize two sets of x and y values as scatter plots and line graphs

import matplotlib.pyplot as plt

x_values = [1, 2, 3, 4, 5]
y_values1 = [1, 3, 3, 3.5, 4]

# Plot these values as a scatter plot and a line graph
plt.plot(x_values, y_values1)
plt.scatter(x_values, y_values1, color='red')

# Now add in a second set of x,y values
x_values2 = [1, 2, 3, 4]
y_values2 = [2, 2.5, 3, 3.5]

plt.plot(x_values2, y_values2)
plt.scatter(x_values2, y_values2, color='blue')

plt.show()