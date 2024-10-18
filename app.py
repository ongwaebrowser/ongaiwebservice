Ifrom flask import Flask, render_template, request, jsonify, session
import requests
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Secret Key
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set session timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# API URL to query the AI service
API_URL = "https://ongai.vercel.app/api/ask?message="

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    
    # Send query to AI service
    try:
        response = requests.get(API_URL + user_input)
        response.raise_for_status()  # Ensure valid response
        data = response.json()
        return jsonify({'response': data.get('answer', 'Error: No response received from AI')})
    except Exception as e:
        return jsonify({'response': f"An error occurred"})

@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears session data
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
