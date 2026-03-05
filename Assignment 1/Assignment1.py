# Instructions
# Build an interactive quiz application that supports asking a user at least five multiple-choice questions.
# The quiz should present each question to the user, present at least four options for the answer (a-d), accept an answer from the user (e.g. "b") and let them know if their answer is correct or not.  
# At the end of the quiz, it should report the final score.  
# The program should not allow a user to enter an invalid response (e.g. if the responses are a-d, any other response, such as "q", should be ignored and the user should be re-prompted).  
# The quiz questions should be kept in a file so that it is easy to add/remove questions or to have sets of questions on different topics
# Additional Requirements
    # 1. Write the history of scores out to a file.
    # 9. Add a timer for each question and give bonus points for the fastest correct quiz answers or total quiz time.

# Import relevant libraries
import time
import json
import random
from string import ascii_lowercase

# Load questions from a JSON file and format as a dictionary where the key is the question and the value is a list of options.
def load_questions(filename):
    with open(filename, 'r') as file:
        questions = json.load(file)
    
    questions_dict = {}
    for item in questions['questions']:
        questions_dict[item['question']] = item['options']
    return questions_dict

questions = load_questions('questions.json')

# Shuffle the questions and options to ensure a different quiz experience each time.
def shuffle_questions(questions):
    shuffled_questions = list(questions.items())
    random.shuffle(shuffled_questions)
    return dict(shuffled_questions)

def shuffle_options(options):
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    return shuffled_options

#  Create a dictionary of labeled answer alternatives (e.g. "a", "b", "c", "d") for the options.
def create_labeled_alternatives(options):
    return dict(zip(ascii_lowercase, options))

# Display the question and its answer options to the user.
def display_question(question_num, question, labeled_alternatives):
    print(f"Question {question_num}:")
    print(question)
    for label, alternative in labeled_alternatives.items():
        print(f" {label}. {alternative}")

# Have users answer the questions
def user_answer(labeled_alternatives):
    while True:
        answer_label = input("Your answer: ").strip().lower()
        if answer_label in labeled_alternatives:
            return labeled_alternatives[answer_label]
        print(f"Invalid input. Please enter one of: {', '.join(labeled_alternatives.keys())}")

# Check the user's answer against the correct answer and keep track of the score.
def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        print("Correct!")
        return True
    else:
        print(f"The answer is '{correct_answer}' not '{user_answer}'.")
        return False

# Run the quiz by loading the questions, shuffling them, and iterating through each question to display it, get the user's answer, check it, and keep track of the score. At the end, report the final score.
def run_quiz(questions):
    shuffled_questions = shuffle_questions(questions)
    question_list = list(shuffled_questions.items())
    
    num_correct = 0
    for num, (question, options) in enumerate(question_list, start=1):
        correct_answer = options[0]
        shuffled_options = shuffle_options(options)
        labeled_alternatives = create_labeled_alternatives(shuffled_options)
        
        display_question(num, question, labeled_alternatives)
        user_answer = user_answer(labeled_alternatives)
        
        if check_answer(user_answer, correct_answer):
            num_correct += 1
        print()
    
    return num_correct

def main():
    num_correct = run_quiz(questions)
    print(f"You got {num_correct} out of {len(shuffle_questions)} correct.")

if __name__ == "__main__":
    main()