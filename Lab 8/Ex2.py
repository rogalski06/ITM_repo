# Create an algorithm to determine if a number entered by a user exists in an array of numbers.

search  = [ 2, 5, 7, 11, 15, 22, 27, 30, 34, 41, 55, 57, 58, 60, 77]
num = int(input("Enter a number to search for: "))
if num in search:
    print("The number exists in the array.")
else:
    print("The number does not exist in the array.")