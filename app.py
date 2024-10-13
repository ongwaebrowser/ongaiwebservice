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

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# API URL to query your AI service
API_URL = "https://ongai.vercel.app/api/ask?message="

# List of words that imply a long, detailed response
LONG_RESPONSE_WORDS = ['discuss', 'explain', 'illustrate', 'give detailed explanation', 'elaborate']

# Function to shorten or simplify the query if it contains long-response words
def simplify_query(user_input):
    # Check if user input contains long-response words
    if any(word in user_input.lower() for word in LONG_RESPONSE_WORDS):
        # Append 'briefly' to the query to ask for concise answers
        return user_input + " briefly"
    return user_input

# Function to extract key points using spaCy
def extract_key_points(user_input):
    # Process the input text with spaCy to extract key points
    doc = nlp(user_input)
    keywords = []
    
    for token in doc:
        # We will consider nouns, proper nouns, and verbs as key points
        if token.pos_ in ['NOUN', 'PROPN', 'VERB']:
            keywords.append(token.text)
    
    # Join the keywords (limiting to a certain number if desired)
    return " ".join(keywords[:20])  # Adjust limit as necessary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    
    # Process the user input to simplify the query
    simplified_query = simplify_query(user_input)

    # If query length exceeds 200 characters, extract key points to avoid API errors
    if len(simplified_query) > 200:
        simplified_query = extract_key_points(simplified_query)
    
    # Call the external API with the processed query
    response = requests.get(API_URL + simplified_query)

    if response.status_code == 200:
        data = response.json()
        answer = markdown2.markdown(data['answer'])
        return jsonify({'response': answer})
    else:
        return jsonify({'response': "I am sorry, the query might require a shorter response. Please simplify it and try again."})

# Option to reset session
@app.route('/reset', methods=['POST'])
def reset_session():
    session.clear()  # Clears the session data, including any dialog history
    return jsonify({"message": "Session reset successfully."})

if __name__ == '__main__':
    app.run(debug=True)
