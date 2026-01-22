# Ask the user to enter their weight in pounts. Convert the weight to kilograms (1 pound = 0.453592 kg).
# Name: Katherine Rogalski
# Date: January 22, 2026

pounds_to_kilograms = 0.453592

weight_in_pounds = input("Please enter your weight in pounds: ")
weight_as_float = float(weight_in_pounds)
weight_in_kilograms = weight_as_float * pounds_to_kilograms
weight_in_kilograms_rounded = round(weight_in_kilograms)

print(f"You entered: {weight_as_float} pounds")
print(f"Your weight in kilograms is: {weight_in_kilograms_rounded} kg")