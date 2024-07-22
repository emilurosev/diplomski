from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import re
from nltk.corpus import stopwords
import string
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


model = BertForSequenceClassification.from_pretrained("../fake_news_classifier")
tokenizer = BertTokenizer.from_pretrained("../fake_news_classifier")

stop = set(stopwords.words('english'))
punctuation = list(string.punctuation)
stop.update(punctuation)

def preprocess_text(text):

    def remove_reuters_prefix(text):
        pattern = r'^[\s\S]*?\(reuters\) - '
        return re.sub(pattern, '', text)

    def strip_html(text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def remove_square_brackets(text):
        return re.sub('\[[^]]*\]', '', text)

    def remove_urls(text):
        return re.sub(r'http\S+', '', text)

    def remove_stopwords(text):
        final_text = []
        for i in text.split():
            if i.strip().lower() not in stop:
                final_text.append(i.strip())
        return " ".join(final_text)

    text = text.lower()
    text = remove_reuters_prefix(text)
    text = strip_html(text)
    text = remove_square_brackets(text)
    text = remove_urls(text)
    text = remove_stopwords(text)

    return text

def predict(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=-1).item()
    return prediction

@app.route('/detect', methods=['POST'])
def detect_fake_news():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    preprocessed_text = preprocess_text(text)
    prediction = predict(preprocessed_text)
    result = 'fake' if prediction == 0 else 'real'
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
