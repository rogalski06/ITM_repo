#!/usr/bin/env python3

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please try again.")


def choose_operation():
    while True:
        op = input("Choose operation (+, -, *, /): ").strip()
        if op in ('+', '-', '*', '/'):
            return op
        print("Invalid operation. Choose one of +, -, *, /.")


def calculate(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


def main():
    print("Simple calculator")
    try:
        while True:
            a = get_number("Enter first number: ")
            b = get_number("Enter second number: ")
            op = choose_operation()

            try:
                result = calculate(a, b, op)
            except ZeroDivisionError as e:
                print("Error:", e)
            else:
                print("Result:", result)

            again = input("Perform another calculation? (y/n): ").strip().lower()
            if again in ('n', 'no'):
                print("Goodbye.")
                break
    except KeyboardInterrupt:
        print("\nGoodbye.")


if __name__ == "__main__":
    main()

first=5
second=7
operation='+'