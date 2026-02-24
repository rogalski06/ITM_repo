recent_purchase = [36.13, 23.87, 183.35, 22.93, 11.62]

budget = 150
total_spent = 0

for purchase in recent_purchase:
    total_spent += purchase
    if total_spent > budget:
        print("This purchase is over budget: ", purchase)
    else:
        print("This purchase is within budget: ", purchase) 


# Create a function for this and write test cases for this and use them to test the function.

def check_budget(purchase, limit):
    if purchase > limit:
        return "over budget"
    else:
        return "within budget"

# Test cases
print(check_budget(36.13, 150))  # within budget
print(check_budget(183.35, 150))  # over budget
print(check_budget(0, 150))  # within budget
print(check_budget(150, 150))  # within budget