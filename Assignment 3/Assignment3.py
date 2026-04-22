# Transform your console-based quiz game from Assignment 1 into an interactive web application

# Import necessary libraries
from flask import Flask, render_template, request, jsonify, session
import json
import random
from string import ascii_lowercase
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'secretkey'

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

@app.route('/')
def home():
    """Display the home page"""
    return render_template('home.html')

@app.route('/start')
def start_quiz():
    # Initialize quiz session
    questions = load_questions()
    shuffled_questions = shuffle_questions(questions)
    question_list = list(shuffled_questions.items())
    
    # Store quiz data in session
    session['questions'] = []
    session['current_question'] = 0
    session['num_correct'] = 0
    session['total_bonus_points'] = 0
    session['total_questions'] = len(question_list)
    
    # Format questions for frontend
    for question, options in question_list:
        # Set correct answer to first option from JSON BEFORE any shuffling
        correct_answer = options[0]  # First option is ALWAYS correct
        
        # Now shuffle the options for display
        shuffled_options = shuffle_options(options)
        labeled_alternatives = alt_labels(shuffled_options)
        
        session['questions'].append({
            'question': question,
            'options': labeled_alternatives,
            'correct_answer': correct_answer
        })
    
    session.modified = True
    return render_template('quiz.html')

@app.route('/api/question/<int:question_num>')
def get_question(question_num):
    if 'questions' not in session or question_num >= len(session['questions']):
        return jsonify({'error': 'Invalid question number'}), 400
    
    q = session['questions'][question_num]
    return jsonify({
        'question_number': question_num + 1,
        'total_questions': session['total_questions'],
        'question': q['question'],
        'options': q['options'],  # This is already a dict with a, b, c, d labels
        'timeout': 10
    })

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_num = data.get('question_number', 0)
    user_answer = data.get('answer')
    time_taken = data.get('time_taken')
    
    if 'questions' not in session or question_num >= len(session['questions']):
        return jsonify({'error': 'Invalid question number'}), 400
    
    q = session['questions'][question_num]
    correct_answer = q['correct_answer']
    is_correct = user_answer == correct_answer
    
    if is_correct:
        session['num_correct'] += 1
        bonus_points = calculate_bonus_points(time_taken)
        session['total_bonus_points'] += bonus_points
    else:
        bonus_points = 0
    
    session.modified = True
    
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'bonus_points': bonus_points,
        'time_taken': round(time_taken, 2) if time_taken else None
    })

@app.route('/api/results')
def get_results():
    if 'questions' not in session:
        return jsonify({'error': 'Quiz not started'}), 400
    
    num_correct = session.get('num_correct', 0)
    total_bonus_points = session.get('total_bonus_points', 0)
    total_questions = session.get('total_questions', 0)
    
    # Save the score
    save_score(num_correct, total_bonus_points, total_questions)
    
    return jsonify({
        'num_correct': num_correct,
        'total_questions': total_questions,
        'bonus_points': total_bonus_points,
        'percentage': round((num_correct / total_questions * 100), 1) if total_questions > 0 else 0
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)