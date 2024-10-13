from flask import Flask, render_template, request, jsonify, session
import requests
import markdown2
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Secret Key - securely stored in the .env file
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set session timeout (e.g., 30 minutes of inactivity)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# API URL to query your AI service
API_URL = "https://ongai.vercel.app/api/ask?message="

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    response = requests.get(API_URL + user_input)
    
    if response.status_code == 200:
        data = response.json()
        answer = markdown2.markdown(data['answer'])
        return jsonify({'response': answer})
    else:
        return jsonify({'response': "...."})

# Option to reset session
@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears the session data, including any dialog history
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
