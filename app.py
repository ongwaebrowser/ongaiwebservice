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
        return jsonify({'response': "I am sorry you are experiencing this, I am instructed to answer shorthand questions for free service users. The error may be due to the following reasons: either your query requires a longer description, or an error occurred while submitting your response. To solve the error, please reformat and simplify your query, such as 'what is...' or open a dialog with greetings like 'hello.' Pro mode with long responses will be available soon as part of a paid service. Thanks for your understanding."})

# Option to reset session
@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears the session data, including any dialog history
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
