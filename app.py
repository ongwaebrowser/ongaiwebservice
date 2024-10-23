from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from datetime import timedelta
from ai import ask as ai_ask, reset as ai_reset  # Import functions from ai.py

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask Secret Key
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set session timeout
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']  # Get user input from form

    # Send query to AI service via ai.py
    try:
        # Call the ask() function from ai.py directly to process the user query
        response = ai_ask(user_input)
        if 'error' in response:
            return jsonify({'response': response['error']})
        return jsonify({'response': response.get('answer', 'Error: retry')})
    except Exception as e:
        return jsonify({'response': f"An error occurred. Please try again later. {str(e)}"})

@app.route('/reset', methods=['POST'])
def reset_session():
    try:
        # Call the reset() function from ai.py to reset the session
        ai_reset()  # Clears AI chat history
        session.clear()  # Clears session data
        return jsonify({"message": "Session reset successfully."})
    except Exception as e:
        return jsonify({"message": f"Failed to reset the session. Try again. {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
