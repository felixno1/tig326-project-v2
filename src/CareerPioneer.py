import pickle
from tensorflow.keras.models import load_model # type: ignore
import numpy as np

# Load LabelEncoder
with open('src/cp_ai_model/assets/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Load TfidfVectorizer
with open('src/cp_ai_model/assets/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load the trained model
loaded_model = load_model('src/cp_ai_model')

def predict_top_n_classes(text, model, vectorizer, label_encoder, n=5):
    text_vector = vectorizer.transform([text]).toarray()
    prediction = model.predict(text_vector)
    top_n_indices = np.argsort(prediction[0])[-n:][::-1]
    top_n_probs = prediction[0][top_n_indices]
    top_n_classes = label_encoder.inverse_transform(top_n_indices)
    results = {top_n_classes[i]: round(top_n_probs[i] * 100, 2) for i in range(len(top_n_classes))}
    return results

def predict_jobs(words, class_amount):
    prompt = ' '.join(words)
    results = predict_top_n_classes(prompt, loaded_model, vectorizer, label_encoder, n=class_amount)
    return results
