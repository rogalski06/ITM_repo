# Flask Quiz Application

This is a web-based version of the Assignment 1 quiz game, built with Flask.

## Features

- 🎮 Interactive web interface for the quiz game
- ⏱️ 10-second timer for each question
- 🎯 Multiple choice questions (a-d options)  
- 🏆 Score tracking with bonus points for fast answers
- 💾 Results saved to `score_history.txt`
- 📱 Responsive design that works on desktop and mobile

## Setup & Installation

1. **Make sure Flask is installed:**
   ```bash
   pip install Flask
   ```

2. **Navigate to the project directory:**
   ```bash
   cd "c:\Users\lihka\OneDrive\UHM\Spring 26\ITM 352\GitHub\ITM_repo"
   ```

3. **Run the Flask application:**
   ```bash
   python quiz_app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## How to Play

1. The quiz will load with the first question
2. Select an answer by clicking on one of the options (a, b, c, or d)
3. Click "Submit Answer" to submit your response
4. You'll see immediate feedback showing if you're correct or incorrect
5. The correct answer will be highlighted
6. Click "Next Question" to move to the next question
7. After all questions, your final score will be displayed
8. Click "Take Quiz Again" to restart the quiz

## Bonus Points System

- **3 points**: Answer in 5 seconds or less
- **2 points**: Answer between 5-8 seconds
- **1 point**: Answer between 8-10 seconds
- **0 points**: Answer after 10 seconds or no answer

## Correct Answer Logic

**The first option in questions.json is always the correct answer.** The options are shuffled for display purposes, but the correct answer is always tracked as the first option from the JSON file.

Example from questions.json:
```json
{
  "question": "What is Lightning McQueen's racing number?",
  "options": ["95", "67", "21", "77"]
}
```
"95" is the correct answer (first option), even though it may appear as option a, b, c, or d after shuffling.

## File Structure

```
ITM_repo/
├── quiz_app.py              # Main Flask application
├── templates/
│   └── quiz.html           # Web interface
├── Assignment 1/
│   ├── Assignment1.py      # Original quiz game
│   └── questions.json      # Quiz questions
└── score_history.txt       # Quiz results log
```

## API Endpoints

- **GET `/`** - Load quiz page
- **GET `/api/question/<int>`** - Get a specific question
- **POST `/api/answer`** - Submit an answer
- **GET `/api/results`** - Get final quiz results

## Customization

To change the quiz questions, edit the `Assignment 1/questions.json` file with new questions and answers. The first option in each question is automatically marked as the correct answer.

## Notes

- The quiz session is stored in Flask sessions (server-side)
- Each session/user gets their own independent quiz
- To reset the app or clear sessions, restart the Flask server
- Correct answer validation compares the exact text of the selected answer with the first option from JSON
