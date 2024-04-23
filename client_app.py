from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get prompt from the form
        prompt = request.form.get('prompt')
        max_length = int(request.form.get('max_length', 50))

        # Make a POST request to the server to generate text
        response = requests.post('http://127.0.0.1:5001/generate', json={'prompt': prompt, 'max_length': max_length})

        # Get the generated text from the response
        generated_text = response.json().get('generated_text')

        return render_template('index.html', generated_text=generated_text)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
