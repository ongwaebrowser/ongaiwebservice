from flask import Flask, render_template, request, jsonify, session
import requests
import os
from dotenv import load_dotenv
from datetime import timedelta
import urllib.parse

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
    
    # URL encode the query to avoid bad request errors
    encoded_input = urllib.parse.quote(user_input)

    # Send query to AI service without timeout to avoid errors
    try:
        response = requests.get(API_URL + encoded_input)
        response.raise_for_status()  # Ensure valid response
        data = response.json()
        return jsonify({'response': data.get('answer', 'Error: retry')})
    except requests.exceptions.Timeout:
        return jsonify({'response': "The request timed out. Please try again."})
    except Exception as e:
        return jsonify({'response': f"An error occurred. Please try again"})

@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears session data
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
