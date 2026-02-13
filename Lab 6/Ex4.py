# A leap year is a year that consists of 366 days, not the usual 365 days. It occurs roughly every four years, with the exception of certain century years. Specifically, a year is a leap year if it is either 1) evenly divisible by 4 but not divisible by 100, or 2) evenly divisible by 400.

# Design a conditional expression for the leap year conditional logic using a combination of AND and OR operators with specific parenthetical grouping (Condition A AND Condition B) OR Condition C. How must you ensure that the boolean operators correctly mirror the flow-chart to prevent unintended evaluation order? Test your program with your own birth year and the closest leap year to your birth year. If your birth year is a leap year, then use your birth year + 1 for the non-leap year. 

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Replace with your birth year
birth_year = 2006
closest_leap_year = 2004

print(f"{birth_year}: {'Leap Year' if is_leap_year(birth_year) else 'Not Leap Year'}")
print(f"{closest_leap_year}: {'Leap Year' if is_leap_year(closest_leap_year) else 'Not Leap Year'}")

# B
def isLeapYear(year):
    # Check divisibility by 4 first (early exit if not divisible)
    if year % 4 != 0:
        return "Not a leap year"
    # Check divisibility by 100 next
    if year % 100 != 0:
        return "Leap year"
    # Check divisibility by 400 last
    if year % 400 == 0:
        return "Leap year"
    else:
        return "Not a leap year"

# Test cases
birth_year = 2006
closest_leap_year = 2000

print(f"{birth_year}: {isLeapYear(birth_year)}")
print(f"{closest_leap_year}: {isLeapYear(closest_leap_year)}")