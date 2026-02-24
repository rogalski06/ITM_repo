# Quiz Game - Version 3
# Katherine Rogalski
# Date: Feb 24, 2026
# Make a list with the questions and correct answers.
# Make questions a dictionary, to include answer options and the correct answer.

questions = {
    "What is the airspeed of an unladen swallow in miles/hour?": ["12", "10", "15", "8"],
    "What is the capital of Texas?": ["Dallas", "Houston", "Austin", "San Antonio"],
    "The last supper was painted by which artist?": ["Michelangelo", "Raphael", "Da Vinci", "Caravaggio"]
}

for question, options in questions.items():
    correct_answer = options[0]
    for alternative in sorted(options):
        print(f" - {alternative}")

    answer = input(question + ": ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}' not '{answer}'.")