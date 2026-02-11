# Create a list with a variety of different values
# Include control logic (if, elif, else) that will print different messages whether the list contains fewer than 5 elements, between 5 and 10 (inclusive), and more than 10 elements. 

list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
if len(list) < 5:
    print("The list contains less than 5 elements.")
elif len(list) >= 5 and len(list) <= 10:
    print("The list contains between 5 and 10 elements.")
else:
    print("The list contains more than 10 elements.")