# Transform your console-based quiz game from Assignment 1 into an interactive web application

# Import necessary libraries
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import random
from string import ascii_lowercase
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secretkey'

# Following definitions are copied from Assignment 1 with modifications for web app

# Load questions from JSON file
def load_questions(filename='questions.json'):
    with open(filename, 'r') as file:
        questions = json.load(file)
    
    return questions['questions']

# Shuffle the questions
def shuffle_questions(questions):
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)
    return shuffled_questions

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
    elif time_taken <= 3:
        return 3
    elif time_taken <= 5:
        return 2
    elif time_taken <= 7:
        return 1
    else:
        return 0

# Save quiz results to history file
def save_score(num_correct, total_bonus, total_questions, username, filename='score_history.txt'):
    timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
    with open(filename, 'a') as f:
        f.write(f"{timestamp} - {username}: {num_correct}/{total_questions} correct, points = {total_bonus}\n")

# Load users from JSON file
def load_users(filename='users.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

# Save users to JSON file
def save_users(users, filename='users.json'):
    with open(filename, 'w') as file:
        json.dump(users, file, indent=2)

# Load user scores
def load_user_scores(username, filename='user_scores.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            all_scores = json.load(file)
            return all_scores.get(username, [])
    return []

# Save user score
def save_user_score(username, score_data, filename='user_scores.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            all_scores = json.load(file)
    else:
        all_scores = {}
    
    if username not in all_scores:
        all_scores[username] = []
    
    all_scores[username].append(score_data)
    
    with open(filename, 'w') as file:
        json.dump(all_scores, file, indent=2)

# Define Flask routes for the web application

# Home page route - requires login
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        if username in users and check_password_hash(users[username]['password_hash'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        if username in users:
            flash('Username already exists')
        else:
            users[username] = {
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now().isoformat()
            }
            save_users(users)
            session['username'] = username
            return redirect(url_for('home'))
    
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Start quiz route - requires login
@app.route('/start')
def start_quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Initialize quiz session
    questions = load_questions()
    shuffled_questions = shuffle_questions(questions)
    
    # Store quiz data in session
    session['questions'] = []
    session['current_question'] = 0
    session['num_correct'] = 0
    session['total_bonus_points'] = 0
    session['total_questions'] = len(shuffled_questions)
    session['missed_questions'] = []  # Track questions answered incorrectly
    
    # Format questions
    for question_data in shuffled_questions:
        # Set correct answer to first option from JSON before shuffling
        correct_answer = question_data['options'][0]  # First option is correct
        
        # Now shuffle the options for display
        shuffled_options = shuffle_options(question_data['options'])
        labeled_alternatives = alt_labels(shuffled_options)
        
        session['questions'].append({
            'question': question_data['question'],
            'options': labeled_alternatives,
            'correct_answer': correct_answer,
            'explanation': question_data.get('explanation', 'No explanation available.')  # Add explanation
        })
    
    session.modified = True
    return render_template('quiz.html')

# Route to get current question and options
@app.route('/api/question/<int:question_num>')
def get_question(question_num):
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
        
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

# Route to submit answer and calculate score
@app.route('/api/answer', methods=['POST'])
def submit_answer():
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
        
    # Get data from request
    data = request.json
    question_num = data.get('question_number', 0)
    user_answer = data.get('answer')
    time_taken = data.get('time_taken')
    
    # Validate input
    if 'questions' not in session or question_num >= len(session['questions']):
        return jsonify({'error': 'Invalid question number'}), 400
    
    # Check if the answer is correct and calculate bonus points
    q = session['questions'][question_num]
    correct_answer = q['correct_answer']
    is_correct = user_answer == correct_answer
    
    if is_correct:
        session['num_correct'] += 1
        bonus_points = calculate_bonus_points(time_taken)
        session['total_bonus_points'] += bonus_points
    else:
        bonus_points = 0
        # Track missed question for review
        missed_question = {
            'question': q['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'explanation': q.get('explanation', 'No explanation available.'),
            'question_number': question_num + 1
        }
        if 'missed_questions' not in session:
            session['missed_questions'] = []
        session['missed_questions'].append(missed_question)
    
    # Mark session as modified to ensure changes are saved
    session.modified = True
    
    # Return response with correctness, correct answer, bonus points, and time taken
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'bonus_points': bonus_points,
        'time_taken': round(time_taken, 2) if time_taken else None
    })

# Results route to display final score and save it to history
@app.route('/api/results')
def get_results():
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
        
    if 'questions' not in session:
        return jsonify({'error': 'Quiz not started'}), 400
    
    # Retrieve final score and save it to history
    num_correct = session.get('num_correct', 0)
    total_bonus_points = session.get('total_bonus_points', 0)
    total_questions = session.get('total_questions', 0)
    username = session['username']
    
    # Save to global history
    save_score(num_correct, total_bonus_points, total_questions, username)
    
    # Save to user-specific scores
    score_data = {
        'timestamp': datetime.now().isoformat(),
        'num_correct': num_correct,
        'total_questions': total_questions,
        'bonus_points': total_bonus_points,
        'percentage': round((num_correct / total_questions * 100), 1) if total_questions > 0 else 0
    }
    save_user_score(username, score_data)
    
    # Return final results
    return jsonify({
        'num_correct': num_correct,
        'total_questions': total_questions,
        'bonus_points': total_bonus_points,
        'percentage': round((num_correct / total_questions * 100), 1) if total_questions > 0 else 0
    })

# Review route - shows missed questions with explanations
@app.route('/review')
def review():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'missed_questions' not in session:
        return redirect(url_for('home'))
    
    missed_questions = session.get('missed_questions', [])
    return render_template('review.html', missed_questions=missed_questions)

# Run the Flask app if it is the main module
if __name__ == '__main__':
    app.run(debug=True, port=5000)