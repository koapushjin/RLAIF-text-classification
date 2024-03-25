import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.linear_model import SGDClassifier


app = Flask(__name__)


# obtain x, y for training
categories = ['alt.atheism', 'soc.religion.christian']
newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(newsgroups_train.data)
y_train = newsgroups_train.target

# initialize model
model = SGDClassifier(loss='log', max_iter=1000, tol=1e-3)
model.partial_fit(X_train, y_train, classes=np.unique(y_train))

# store labeled text
predicted_text = []
corrected_text = []


def store_predicted_text(text, prediction, confidence):
    predicted_text.append(
        {'text': text, 'prediction': prediction, 'confidence': confidence})


def store_corrected_text(text, corrected_label):
    corrected_text.append({'text': text, 'prediction': corrected_label})


def compute_entropy(confidence):
    return - confidence * np.log2(confidence) - (1 - confidence) * np.log2(1 - confidence)


def update_model(feedback_text, corrected_label):
    feedback_vectorized = vectorizer.transform([feedback_text])
    model.partial_fit(feedback_vectorized, np.array([corrected_label]))


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['text']
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    confidence = max(model.predict_proba(text_vectorized)[0])
    store_predicted_text(text, int(prediction), float(confidence))
    predicted_label = "Atheism" if newsgroups_train.target_names[
        prediction] == 'alt.atheism' else "Christian"
    entropy = compute_entropy(confidence)
    print(confidence, entropy)
    return jsonify({'prediction': predicted_label, 'confidence': confidence})
    # return jsonify({'prediction': predicted_label, 'confidence': confidence, 'entropy': entropy})


@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    text = data['text']
    corrected_label = categories.index(data['label'])
    store_corrected_text(text, int(corrected_label))
    update_model(text, corrected_label)
    return jsonify({'message': 'Annotation received and model updated.'})


@app.route('/')
def home():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
