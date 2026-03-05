# Quiz Game - Version 4
# Katherine Rogalski
# Date: Feb 24, 2026
# Make a list with the questions and correct answers.
# Make questions a dictionary, to include answer options and the correct answer.
# Allow the user to select the correct answer by a label.

questions = {
    "What is the airspeed of an unladen swallow in miles/hour?": ["12", "10", "15", "8"],
    "What is the capital of Texas?": ["Austin", "Houston", "Dallas", "San Antonio"],
    "The last supper was painted by which artist?": ["Da Vinci", "Raphael", "Michelangelo", "Caravaggio"]
}

for question, options in questions.items():
    correct_answer = options[0]
    sorted_options = sorted(options)
    for label, alternative in enumerate(sorted_options, start=1):
        print(f" {label}. {alternative}")

    answer_label = int(input(question + ": "))

    answer = sorted_options[answer_label - 1]
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}' not '{answer}'.")