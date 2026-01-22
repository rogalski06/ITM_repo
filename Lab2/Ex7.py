# Ask the user to enter a temperature in fehrenheit. Convert the temperature to celsius (C = (F - 32) * 5/9).
# Name: Katherine Rogalski
# Date: January 22, 2026

fehrenheit_input = input("Please enter a temperature in fehrenheit: ")
fehrenheit_value = float(fehrenheit_input)
celsius_value = (fehrenheit_value - 32) * 5 / 9
celsius_value_rounded = round(celsius_value, 1)

print(f"You entered: {fehrenheit_value} °F")
print(f"Temperature in Celsius: {celsius_value_rounded} °C")