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
        return jsonify({'response': "I am sorry you are experiencing this problem. As a mini Ai, am trained to answer shorthand questions like start by 'what is...'.The error may be resolved by reformatting your search question or use key words. Minor possible causes may include connectivity and busy response mode."})

if __name__ == '__main__':
    app.run(debug=True)
