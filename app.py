from flask import Flask, render_template, request, jsonify, session
import requests
import markdown2
import os
from dotenv import load_dotenv
from datetime import timedelta
import spacy

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Secret Key - securely stored in the .env file
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set session timeout (e.g., 30 minutes of inactivity)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# API URL to query your AI service
API_URL = "https://ongai.vercel.app/api/ask?message="

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Keywords to identify long or descriptive queries
LONG_QUERY_KEYWORDS = ["discuss", "explain", "illustrate", "give detailed explanation", "describe", "elaborate"]

# Function to simplify a long query
def simplify_query(user_input):
    doc = nlp(user_input)
    # Check if any of the long query keywords are present in the user input
    if any(keyword in user_input.lower() for keyword in LONG_QUERY_KEYWORDS):
        # Simplify the input by extracting keywords (nouns, verbs, etc.)
        keywords = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "PROPN", "ADJ")]
        return " ".join(keywords) + " briefly"
    return user_input  # Return the original input if it's already short

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    
    # Simplify the query if it's too long or contains keywords that need to be summarized
    simplified_query = simplify_query(user_input)
    
    # Send the simplified query to the API
    response = requests.get(API_URL + simplified_query)
    
    if response.status_code == 200:
        data = response.json()
        answer = markdown2.markdown(data['answer'])
        return jsonify({'response': answer})
    else:
        return jsonify({'response': "I am sorry you are experiencing this..."})

# Option to reset session
@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears the session data, including any dialog history
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
