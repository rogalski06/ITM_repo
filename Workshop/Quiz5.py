# Quiz Game - Version 4
# Katherine Rogalski
# Date: Feb 24, 2026
# Make a list with the questions and correct answers.
# Make questions a dictionary, to include answer options and the correct answer.
# Allow the user to select the correct answer by a label.
# Improve look and usability. Keep track of correct answers.

from string import ascii_lowercase

questions = {
    "What is the airspeed of an unladen swallow in miles/hour?": ["12", "10", "15", "8"],
    "What is the capital of Texas?": ["Austin", "Houston", "Dallas", "San Antonio"],
    "The last supper was painted by which artist?": ["Da Vinci", "Raphael", "Michelangelo", "Caravaggio"]
}

num_correct = 0
for num, (question, options) in enumerate(questions.items(), start=1):
    print(f"Question {num}:")
    print(question)
    correct_answer = options[0]
    labeled_alternatives = dict(zip(ascii_lowercase, sorted(options)))
    for label, alternative in labeled_alternatives.items():
        print(f" {label}. {alternative}")

    answer_label = input("Your answer: ")
    answer = labeled_alternatives.get(answer_label)
    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer}' not '{answer}'.")

print(f"You got {num_correct} out of {len(questions)} correct.")