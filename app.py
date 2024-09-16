from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)


sentiment_classifier = pipeline("sentiment-analysis")
text_generator = pipeline("text-generation", model="gpt2")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    
    result = sentiment_classifier(text)[0]
    sentiment = result['label']
    score = result['score']

    if sentiment == 'POSITIVE':
       
        prompt = f"Expand on this positive way: {text}"
        generated_text = text_generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
        response_message = f" Here's an expanded version: {generated_text}"
    else:
        
        prompt = f"Rephrase this negative thought in a positive way: {text}"
        generated_text = text_generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
        response_message = f"Here's a more positive version: {generated_text}"

    
    response = {
        'sentiment': sentiment,
        'score': score,
        'message': response_message
    }

    return jsonify(response)  

if __name__ == '__main__':
    app.run(debug=True)

