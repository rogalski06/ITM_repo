# Read the 1,000 lines of taxi data from the taxi_1000.csv file
# Calculate the total of all fares, average fare, and the max trip distance for fares over $10.00

import csv
import os

filename = "..\\taxi_1000.csv"
with open(filename) as csvfile:
    csv_reader = csv.reader(csvfile)

    total_fare = 0.0
    max_distance = 0.0
    average_fare = 0.0
    num_rows = 0

    for line in csv_reader:
        if (num_rows == 0):
            fare_index = line.index("Fare")
            distance_index = line.index("Trip Miles")
            num_rows += 1
            continue
        if (num_rows > 0): # Skip the header row
            trip_fare = float(line[fare_index])
            trip_distance = float(line[distance_index])
            if trip_fare > 10:
                total_fare += trip_fare
                if (trip_distance > max_distance):
                    max_distance = trip_distance
                num_rows += 1

    if (num_rows > 0):
        average_fare = total_fare / (num_rows -1)

    print(f"We read {num_rows - 1} qualifying rows of data (fares > $10)")
    print(f"Total Fare: ${total_fare:.2f}")
    print(f"Average Fare: ${average_fare:.2f}")
    print(f"Max Trip Distance: {max_distance:.2f} miles")