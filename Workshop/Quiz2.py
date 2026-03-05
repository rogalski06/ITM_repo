# Quiz Game - Version 2
# Katherine Rogalski
# Date: Feb 24, 2026
# Make a list with the questions and correct answers.

questions = [
    ("What is the airspeed of an unladen swallow in miles/hour?", "12"),
    ("What is the capital of Texas?", "Austin"),
    ("The last supper was painted by which artist?", "Da Vinci")
]

for question, correct_answer in questions:
    answer = input(question + ": ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}' not '{answer}'.")