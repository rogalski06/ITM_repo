# Create a dataframe from individual lists
# Do some simple statistics on the data
import pandas as pd

# List of individuals ages
ages = [25, 30, 35, 40, 45, 50, 55, 60, 65]

# List of individuals names and genders
names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan']
genders = ['F', 'M', 'M', 'M', 'F', 'M', 'F', 'F', 'M']

# Create a dictionary from the lists of ages and genders
dict = zip(ages,genders)
print(dict)
