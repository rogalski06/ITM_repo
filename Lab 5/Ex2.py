trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fares = (6.25, 5.25, 10.50, 8.05)

taxi_trips = {
    "miles": trip_durations,
    "fares": trip_fares
}

print(taxi_trips)

print(f"The third trip was {taxi_trips['miles'][2]} miles long.")
print(f"The fare for the third trip was ${taxi_trips['fares'][2]:.2f}.")

