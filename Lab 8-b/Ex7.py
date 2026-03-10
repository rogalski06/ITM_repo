# Algorithm for multiplying two numbers by successive addition.

def multiply(x, y):
   product = x
   for x in range(y):
       product *= product
  
   return y

first = input("Enter the first number: ")
second = input("Enter the second number: ")
prod = multiply(first, second)

print(f"The product of {first}, {second} is {prod}")
