# An example of creating and using your own function.
# Name: Katherine Rogalski
# Date: January 22, 2026
import datetime

def greet(name):
    """This function greets the person whose name is passed in. In addition we want to print a welcome message that includes the day of the week."""
    message = "Hello" + " " + name + "!"
    x = datetime.datetime.now()
    day_of_week = x.strftime("%A")
    message += " Happy " + day_of_week + "!"
    return message

user_name = input("Please enter your name: ")
greeting_message = greet(user_name)
print(greeting_message)