# This program demonstrates variable scope in Python.
# Name: Katherine Rogalski
# Date: January 27, 2026

def calculate_discounted_price(price, discount):
    price = price * discount
    print(f"Inside function, discounted price: {price:.2f}")
    return price

price = 100
discount = 0.9
print(f"Original price before function call: {price:.2f}")
discounted_price = calculate_discounted_price(price)

print(f"Original price after function call: {price:.2f}")
print ("Discount = ", discount)

