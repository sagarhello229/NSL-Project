from flask import Flask, request, jsonify, send_file
from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_image
import numpy as np
import cv2
from gtts import gTTS
import os
import uuid

app = Flask(__name__)


model = load_model('/home/sagar/Code/project-3/nsl_dataset/NSL_Model.keras')
print("Model loaded successfully")

classes = [
    'ज्ञ', 'क', 'क्ष', 'ख', 'ग', 'घ',
    'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
    'ट', 'ठ', 'ड', 'ढ', 'ण',
    'त', 'त्र्', 'थ', 'द', 'ध', 'न',
    'प', 'फ', 'ब', 'भ', 'म',
    'य', 'र', 'ल', 'व', 'श',
    'ष', 'स', 'ह'
]

CONFIDENCE_THRESHOLD = 0.90

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({'error': 'Failed to decode image'}), 400

    processed = preprocess_image(image) 

    predictions = model.predict(processed)[0]
    label_index = np.argmax(predictions)
    confidence = float(predictions[label_index])
    label = classes[label_index]

    print(f"Predicted: {label} with confidence {confidence}")

    if confidence < CONFIDENCE_THRESHOLD:
        return jsonify({'label': None, 'confidence': confidence})

    return jsonify({'label': label, 'confidence': confidence})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    tts = gTTS(text=text, lang='ne')

    os.makedirs('static', exist_ok=True)
    fname = f'static/{uuid.uuid4().hex}.mp3'
    tts.save(fname)

    
    if not os.path.isfile(fname):
        return jsonify({'error': 'Audio file could not be created'}), 500

    return send_file(fname, mimetype='audio/mpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
