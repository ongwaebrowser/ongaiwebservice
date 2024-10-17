from flask import Flask, render_template, request, jsonify, session
import requests
import markdown2
import os
from dotenv import load_dotenv
from datetime import timedelta
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Secret Key – securely stored in the .env file
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set session timeout (e.g., 30 minutes of inactivity)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# API URL to query your AI service
API_URL = "https://ongai.vercel.app/api/ask?message="

# Keywords to identify long or descriptive queries
LONG_QUERY_KEYWORDS = ["discuss", "explain", "illustrate", "give detailed explanation", "describe", "elaborate", "analyze"]

# Function to simplify a long query
def simplify_query(user_input):
    """
    This function simplifies user input if it contains any long-query keywords like "discuss," 
    "explain," etc. It reduces the query to important words (nouns/verbs) and appends the word 'briefly.'
    """
    # Convert user input to lowercase and check if it contains any of the long-query keywords
    if any(keyword in user_input.lower() for keyword in LONG_QUERY_KEYWORDS):
        # If a long-query keyword is found, simplify the input by extracting important words
        important_words = re.findall(r'\b[a-zA-Z]{4,}\b', user_input)  # Captures words with 4 or more letters
        simplified_query = " ".join(important_words) + " briefly"  # Rebuilds the query and adds 'briefly'
        return simplified_query
    # If no long-query keyword is found, return the original input
    return user_input

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    
    # Simplify the user query if it contains keywords indicating a long query
    simplified_query = simplify_query(user_input)
    
    # Send the simplified query to the AI API
    response = requests.get(API_URL + simplified_query)
    
    # Process the response from the API
    if response.status_code == 200:
        data = response.json()
        answer = markdown2.markdown(data['answer'])
        return jsonify({'response': answer})
    else:
        # Error response if the query fails or is too long
        return jsonify({'response': "I am sorry you are experiencing this. I am instructed to answer shorthand questions for free service users. The error may be due to the following reasons: either your query requires a longer description, or an error occurred while submitting your response. Please reformat and simplify your query, such as 'Discuss...', 'explain...' or start a dialog with greetings like 'hello.' Pro mode with long responses will be available soon as part of a paid service. Thanks for your understanding."})

# Option to reset session
@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears session data, including any dialog history
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
