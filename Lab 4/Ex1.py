# String manipulation examples

first = input("Enter your first name: ")
middle = input("Enter your middle initial: ")
last = input("Enter your last name: ")

full_name = first + " " + middle + ". " + last
print("Your full name is:", full_name)

print(f"Your full name is: {first} {middle}. {last}")

print("Your full name is: %s %s. %s" % (first, middle, last))

print("Your full name is: {} {}. {}".format(first, middle, last))

parts = [first, middle, last]
print("Your full name is: {} {}. {}".format(*parts))

parts_join = [first, middle + '.', last]
print("Your full name is:", " ".join(parts_join))

