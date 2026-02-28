# Quiz Game - Version 7
# Katherine Rogalski
# Date: Feb 27, 2026
# Make a list with the questions and correct answers.
# Make questions a dictionary, to include answer options and the correct answer.
# Allow the user to select the correct answer by a label.
# Improve look and usability. Keep track of correct answers.
# Randomize the order of questions and order of the answer alternatives per question.
# Refactor the code to use functions
# Put the questions into a JSON file and read from it.

from string import ascii_lowercase
import random
import json
import os


def load_questions(filename):
    """Load questions from a JSON file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Convert list of question dicts to the expected format
    questions = {}
    for item in data['questions']:
        questions[item['question']] = item['options']
    
    return questions


questions = load_questions('questions.json')

def shuffle_questions(questions):
    """Create a shuffled copy of the questions."""
    shuffled_questions = list(questions.items())
    random.shuffle(shuffled_questions)
    return dict(shuffled_questions)

def shuffle_options(options):
    """Create a shuffled copy of the answer options."""
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    return shuffled_options


def create_labeled_alternatives(options):
    """Create a dictionary of labeled answer alternatives."""
    return dict(zip(ascii_lowercase, options))


def display_question(question_num, question, labeled_alternatives):
    """Display the question and its answer options."""
    print(f"Question {question_num}:")
    print(question)
    for label, alternative in labeled_alternatives.items():
        print(f" {label}. {alternative}")


def get_user_answer(labeled_alternatives):
    """Get and validate user's answer."""
    while True:
        answer_label = input("Your answer: ").strip().lower()
        if answer_label in labeled_alternatives:
            return labeled_alternatives[answer_label]
        print(f"Invalid input. Please enter one of: {', '.join(labeled_alternatives.keys())}")


def check_answer(user_answer, correct_answer):
    """Check if the user's answer is correct and provide feedback."""
    if user_answer == correct_answer:
        print("Correct!")
        return True
    else:
        print(f"The answer is '{correct_answer}' not '{user_answer}'.")
        return False


def run_quiz(questions):
    """Run the quiz and return the number of correct answers."""
    shuffled_questions = shuffle_questions(questions)
    question_list = list(shuffled_questions.items())
    
    num_correct = 0
    for num, (question, options) in enumerate(question_list, start=1):
        correct_answer = options[0]
        shuffled_options = shuffle_options(options)
        labeled_alternatives = create_labeled_alternatives(shuffled_options)
        
        display_question(num, question, labeled_alternatives)
        user_answer = get_user_answer(labeled_alternatives)
        
        if check_answer(user_answer, correct_answer):
            num_correct += 1
        print()  # Blank line for readability
    
    return num_correct


def main():
    """Main entry point for the quiz game."""
    num_correct = run_quiz(questions)
    print(f"You got {num_correct} out of {len(questions)} correct.")


if __name__ == "__main__":
    main()