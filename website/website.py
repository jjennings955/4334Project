from flask import Flask, render_template, request, jsonify
import pandas as pd
import subprocess
import joblib
from nltk.tokenize import RegexpTokenizer, punkt

tokenizer = RegexpTokenizer("[a-zA-Z]+")
punkt_tok = punkt.PunktSentenceTokenizer()

def tokenize(x):
    return tokenizer.tokenize(x)
from reverb import tokenize, ReverbClassifier
rev = ReverbClassifier()
app = Flask(__name__)

#data = pd.read_csv('')

@app.route('/')
def main(id=0):
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    text = request.form['text']

    sentences = punkt_tok.tokenize(text)
    out = []
    for sentence in sentences:
        words = tokenize(sentence)
        cleaned = ' '.join(words) + '.'
        out.append(cleaned)
    result = list(rev.get_tuples(out))
    return jsonify(dict(zip(range(len(result)), result)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)