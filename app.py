from flask import Flask, render_template, request, jsonify, session
import requests
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Secret Key for session encryption
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set session timeout (30 minutes of inactivity)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# API URL for querying the AI service
API_URL = "https://ongai.vercel.app/api/ask?message="

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    
    # Send the query to the AI API
    response = requests.get(API_URL + user_input)
    
    # Process the response from the API
    if response.status_code == 200:
        data = response.json()
        return jsonify({'response': data['answer']})
    else:
        return jsonify({'response': 'An error occurred while processing your query.'})

# Option to reset session
@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clear session data
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
