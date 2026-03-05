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
import random
from string import ascii_lowercase
import json
import time
from threading import Timer, Thread

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

#Shuffle the options within each question to ensure a different quiz experience each time.
def shuffle_options(options):
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    return shuffled_options

#  Create a dictionary of labeled answer alternatives (e.g. "a", "b", "c", "d") for the options.
def alt_labels(options):
    return dict(zip(ascii_lowercase, options))

# Display the question and its answer options to the user.
def display_question(question_num, question, labeled_alternatives):
    print(f"Question {question_num}:")
    print(question)
    for label, alternative in labeled_alternatives.items():
        print(f" {label}. {alternative}")

# Have users answer the questions with a 10-second timer
def get_user_answer(labeled_alternatives, timeout=10):
    user_answer = [None]
    time_taken = [None]
    start_time = time.time()
    time_exceeded = [False]
    
    def get_input():
        while True:
            if time_exceeded[0]:
                return
            answer_label = input("Your answer: ").strip().lower()
            if answer_label in labeled_alternatives:
                user_answer[0] = labeled_alternatives[answer_label]
                time_taken[0] = time.time() - start_time
                break
            print(f"Invalid input. Please enter one of: {', '.join(labeled_alternatives.keys())}")
    
    def timeout_handler():
        time_exceeded[0] = True
    
    # Start input thread
    input_thread = Thread(target=get_input, daemon=True)
    input_thread.start()
    
    # Start timer
    timer = Timer(timeout, timeout_handler)
    timer.start()
    
    # Wait for input thread to finish or timeout
    input_thread.join(timeout=timeout + 1)
    timer.cancel()
    
    return user_answer[0], time_taken[0]

# Check the user's answer against the correct answer and keep track of the score.
def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        print("Correct!")
        return True
    else:
        print(f"The answer is '{correct_answer}' not '{user_answer}'.")
        return False

# Calculate bonus points based on response time
def calculate_bonus_points(time_taken):
    if time_taken is None:
        return 0  # No answer provided
    elif time_taken <= 5:
        return 3  # 3 points for answering in 5 seconds
    elif time_taken <= 8:
        return 2  # 2 points for answering in 8 seconds
    elif time_taken <= 10:
        return 1  # 1 point for answering in 10 seconds
    else:
        return 0  # No bonus points

# Run the quiz by loading the questions, shuffling them, and iterating through each question to display it, get the user's answer within 10 second timer, check it, and keep track of the score. At the end, report the final score.
def run_quiz(questions):
    shuffled_questions = shuffle_questions(questions)
    question_list = list(shuffled_questions.items())
    
    num_correct = 0
    total_bonus_points = 0
    for num, (question, options) in enumerate(question_list, start=1):
        correct_answer = options[0]
        shuffled_options = shuffle_options(options)
        labeled_alternatives = alt_labels(shuffled_options)
        
        display_question(num, question, labeled_alternatives)
        user_answer, time_taken = get_user_answer(labeled_alternatives)
        
        if user_answer is None:
            print(f"Time's up! The correct answer is '{correct_answer}'.")
        else:
            if check_answer(user_answer, correct_answer):
                num_correct += 1
                bonus_points = calculate_bonus_points(time_taken)
                total_bonus_points += bonus_points
                print(f"Time taken: {time_taken:.2f}s | Bonus points: +{bonus_points}")
            else:
                bonus_points = 0
        print()
    
    return num_correct, total_bonus_points

# Main function to run the quiz and report the final score.
def main():
    num_correct, total_bonus_points = run_quiz(questions)
    print(f"You got {num_correct} out of {len(questions)} correct.")
    print(f"Bonus points earned: {total_bonus_points}")

# Run the main function when the script is executed.
if __name__ == "__main__":
    num_correct, total_bonus_points = run_quiz(questions)
    print(f"Your final score is {num_correct} out of {len(questions)}.")
    print(f"Bonus points earned: {total_bonus_points}")