from flask import Flask, render_template, request, jsonify, session
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
API_URL = "https://ongai.vercel.app/api/ask?message="  # The endpoint URL

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']  # Get input from the form

    # Ensure the user input is not empty before sending the request
    if not user_input.strip():
        return jsonify({'response': 'Please enter a valid query.'})

    try:
        # Send query to AI service without a timeout, and passing 'message' as the query parameter
        response = requests.get(API_URL + user_input)
        response.raise_for_status()  # Ensure the response is valid (status 200)

        # Parse the JSON response
        data = response.json()

        # Return the AI response or error
        if 'answer' in data:
            return jsonify({'response': data['answer']})
        else:
            return jsonify({'response': 'retry.'})

    except requests.exceptions.RequestException as e:
        return jsonify({'response': f"An error occurred: {str(e)}"})

@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears session data
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
