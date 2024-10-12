from flask import Flask, render_template, request, jsonify
import requests
import markdown2

app = Flask(__name__)

API_URL = "https://ongai.vercel.app/api/ask?message="

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    user_input = request.form['query']
    
    # Limit query length for free users
    if len(user_input) > 500:  # Adjust the length as needed
        return jsonify({
            'response': "Your query is too long for the free service. Please simplify your query or consider waiting for the pro mode with longer responses."
        })

    try:
        # Call the external API
        response = requests.get(API_URL + user_input)
        
        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            answer = markdown2.markdown(data['answer'])
            return jsonify({'response': answer})
        else:
            # Generic message when response fails
            return jsonify({
                'response': "An unexpected error occurred while processing your query. Please try simplifying your request, or try again later. Thanks for your understanding!"
            })

    except requests.exceptions.RequestException as e:
        # Log the exception internally, don't show the error to the user
        print(f"API Error: {str(e)}")  # This will only show in your logs/console

        return jsonify({
            'response': "There was an issue processing your request. Please try again later or simplify your query for a better response."
        })

if __name__ == '__main__':
    app.run(debug=True)
