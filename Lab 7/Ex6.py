# Write code that will try to append an input from the user to the tuple that you created in Exercise 3 and print out the appended tuple.

#ex3_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5, 6.7, True)

#user_input = input("Enter a value to append to the tuple: ")

#ex3_tuple.append(user_input) 

# Append list instead
ex3_list = ["hello", 10, "goodbye", 3, "goodnight", 5, 6.7, True]
user_input = input("Enter a value to append to the list: ")
ex3_list.append(user_input)
print("Updated list:", ex3_list)

# Modify your code using try and except statements to handle this error, reporting to the user that an attempt was made to append a value to the tuple. Get the error from the exception and print this with the report.

ex3_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5, 6.7, True)
user_input = input("Enter a value to append to the tuple: ")
try:
    ex3_tuple.append(user_input)
except AttributeError as Message:
    print("An attempt was made to append a value to the tuple.")
    print("Error message:", Message)

# Instead of reporting an error in the exception, handle it by creating a new tuple by adding the input to the tuple and then assigning it back to the variable holding the tuple. The program should not exit and will continue to the end printing out the appended tuple.

ex3_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5, 6.7, True)
user_input = input("Enter a value to append to the tuple: ")
try:
    ex3_tuple.append(user_input)
except AttributeError:
    ex3_tuple = ex3_tuple + (user_input,)
    print("Value appended to the tuple.")
    print("Updated tuple:", ex3_tuple)

# Instead of adding, use the unpacking operator (*) to append the value
ex3_tuple = ("hello", 10, "goodbye", 3, "goodnight", 5, 6.7, True)
user_input = input("Enter a value to append to the tuple: ")
try:
    ex3_tuple.append(user_input)
except AttributeError:
    ex3_tuple = (*ex3_tuple, user_input)
    print("Value appended to the tuple.")
    print("Updated tuple:", ex3_tuple)