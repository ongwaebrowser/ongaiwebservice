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
    response = requests.get(API_URL + user_input)
    
    if response.status_code == 200:
        data = response.json()
        answer = markdown2.markdown(data['answer'])
        return jsonify({'response': answer})
    else:
        return jsonify({'response': "I am sorry you are experiencing this,I am instructed to answer shorthand questions for free service users.The error may be due to the following reasons, either your query requires a longer description or some error occured on submitting your response.To solve the error, reformat and simplify your query like'what is..' or open a dialog with greetings' hello' and for efficiency use key terms.a pro mode will be available in some days in future which will have long responses in a paid program.Thanks for your understanding😊."})

if __name__ == '__main__':
    app.run(debug=True)
