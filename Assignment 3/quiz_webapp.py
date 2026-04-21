from flask import Flask, json, redirect, render_template, request, url_for
import json
import random
from string import ascii_lowercase
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 1
        # Logic to capture the user’s answers and redirect to the result page
        # return redirect(url_for('result'))
        return render_template('result.html', score=score)
    else:
    # Load the question and options to display
        return render_template('quiz.html')  # Displays the question and options

@app.route('/result')
def result():
    # Calculate and display the user's score
    score = 1  # Example score for demonstration
    return render_template('result.html', score=score)

# Load questions from JSON file
def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    
    questions_dict = {}
    for item in questions['questions']:
        questions_dict[item['question']] = item['options']
    return questions_dict

# Shuffle the questions
def shuffle_questions(questions):
    shuffled_questions = list(questions.items())
    random.shuffle(shuffled_questions)
    return dict(shuffled_questions)

# Shuffle options within each question
def shuffle_options(options):
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    return shuffled_options

# Create labeled answer alternatives (a, b, c, d)
def alt_labels(options):
    return dict(zip(ascii_lowercase, options))

# Calculate bonus points based on response time
def calculate_bonus_points(time_taken):
    if time_taken is None:
        return 0
    elif time_taken <= 5:
        return 3
    elif time_taken <= 8:
        return 2
    elif time_taken <= 10:
        return 1
    else:
        return 0

# Save quiz results to history file
def save_score(num_correct, total_bonus, total_questions, filename='score_history.txt'):
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    with open(filename, 'a') as f:
        f.write(f"{timestamp} - {num_correct}/{total_questions} correct, points = {total_bonus}\n")

if __name__ == '__main__':
    app.run(debug=True)
