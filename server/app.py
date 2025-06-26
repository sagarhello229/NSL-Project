from flask import Flask, request, jsonify, send_file
import numpy as np
import joblib
import cv2
import os
import uuid
from gtts import gTTS

app = Flask(__name__)

svm_model = joblib.load("/home/sagar/Code/project-3/nsl_dataset/final_svm_model.pkl")
pca_transformer = joblib.load("/home/sagar/Code/project-3/nsl_dataset/final_svm_pca_model.pkl")
label_encoder = joblib.load("/home/sagar/Code/project-3/nsl_dataset/svm_label_encoder.pkl")
print("Model loaded successfully.")

CONFIDENCE_THRESHOLD = 0.6

def preprocess_and_predict(image):
    try:
        image = cv2.resize(image, (64, 64))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype("float32") / 255.0
        flat = image.reshape(1, -1)

        transformed = pca_transformer.transform(flat)

        probabilities = svm_model.predict_proba(transformed)[0]
        pred_idx = np.argmax(probabilities)
        confidence = probabilities[pred_idx]

        if confidence < CONFIDENCE_THRESHOLD:
            label = None
        else:
            label = label_encoder.inverse_transform([pred_idx])[0]

        print(f"Predicted: '{label}' with confidence {confidence:.4f}")
        return label, confidence

    except Exception as e:
        raise ValueError(f"Preprocessing or prediction failed: {str(e)}")
    
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({'error': 'Invalid image'}), 400

    try:
        label, confidence = preprocess_and_predict(image)
        if confidence < CONFIDENCE_THRESHOLD:
            return jsonify({'label': None, 'confidence': confidence})
        return jsonify({'label': label, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400


    text = data['text'].strip()
    if not text:
        return jsonify({'error': 'Empty text'}), 400

    try:
        tts = gTTS(text=text, lang='ne')
        os.makedirs('static', exist_ok=True)
        fname = f'static/{uuid.uuid4().hex}.mp3'
        tts.save(fname)

        if not os.path.exists(fname):
            return jsonify({'error': 'Failed to create audio'}), 500

        return send_file(fname, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': f'TTS failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



# paxi ko knn ko lagi
# from flask import Flask, request, jsonify, send_file
# import numpy as np
# import joblib
# import cv2
# import os
# import uuid
# from gtts import gTTS

# app = Flask(__name__)

# knn_model = joblib.load("/home/sagar/Code/project-3/nsl_dataset/final_knn_model.pkl")
# pca_transformer = joblib.load("/home/sagar/Code/project-3/nsl_dataset/final_pca_model.pkl")
# label_encoder = joblib.load("/home/sagar/Code/project-3/nsl_dataset/label_encoder.pkl")
# print("Model loaded successfully.")

# CONFIDENCE_THRESHOLD = 0.60

# def preprocess_and_predict(image):
#     try:
#         image = cv2.resize(image, (64, 64))
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image = image.astype("float32") / 255.0
#         flat = image.reshape(1, -1)

#         transformed = pca_transformer.transform(flat)

#         probabilities = knn_model.predict_proba(transformed)[0]
#         pred_idx = np.argmax(probabilities)
#         confidence = probabilities[pred_idx]

#         if confidence < CONFIDENCE_THRESHOLD:
#             label = None
#         else:
#             label = label_encoder.inverse_transform([pred_idx])[0]

#         print(f"Predicted: '{label}' with confidence {confidence:.4f}")
#         return label, confidence

#     except Exception as e:
#         raise ValueError(f"Preprocessing or prediction failed: {str(e)}")
    
# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file provided'}), 400

#     file = request.files['image']
#     npimg = np.frombuffer(file.read(), np.uint8)
#     image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     if image is None:
#         return jsonify({'error': 'Invalid image'}), 400

#     try:
#         label, confidence = preprocess_and_predict(image)
#         if confidence < CONFIDENCE_THRESHOLD:
#             return jsonify({'label': None, 'confidence': confidence})
#         return jsonify({'label': label, 'confidence': confidence})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/speak', methods=['POST'])
# def speak():
#     data = request.get_json()
#     if not data or 'text' not in data:
#         return jsonify({'error': 'No text provided'}), 400

#     text = data['text'].strip()
#     if not text:
#         return jsonify({'error': 'Empty text'}), 400

#     try:
#         tts = gTTS(text=text, lang='ne')
#         os.makedirs('static', exist_ok=True)
#         fname = f'static/{uuid.uuid4().hex}.mp3'
#         tts.save(fname)

#         if not os.path.exists(fname):
#             return jsonify({'error': 'Failed to create audio'}), 500

#         return send_file(fname, mimetype='audio/mpeg')
#     except Exception as e:
#         return jsonify({'error': f'TTS failed: {str(e)}'}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)




# first wala
# from flask import Flask, request, jsonify, send_file
# import numpy as np
# import joblib
# import cv2
# import os
# import uuid
# from gtts import gTTS

# app = Flask(__name__)

# knn_model = joblib.load("/home/sagar/Code/project-3/nsl_dataset/knn_model.pkl")
# pca_transformer = joblib.load("/home/sagar/Code/project-3/nsl_dataset/pca_model.pkl")
# print("Model loaded successfully.")

# CONFIDENCE_THRESHOLD = 0.50

# def preprocess_and_predict(image):
#     try:
#         image = cv2.resize(image, (64, 64))
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image = image.astype("float32") / 255.0
#         flat = image.reshape(1, -1)
#         transformed = pca_transformer.transform(flat)

#         pred_idx = knn_model.predict(transformed)[0]
#         distances, _ = knn_model.kneighbors(transformed)
#         confidence = 1.0 / (distances[0][0] + 1e-5)
#         confidence = min(confidence, 1.0)
#         label = str(pred_idx)  # No label encoder used

#         print(f"Predicted: '{label}' with confidence {confidence:.4f}")

#         return label, confidence
#     except Exception as e:
#         raise ValueError(f"Preprocessing or prediction failed: {str(e)}")

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file provided'}), 400

#     file = request.files['image']
#     npimg = np.frombuffer(file.read(), np.uint8)
#     image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     if image is None:
#         return jsonify({'error': 'Invalid image'}), 400

#     try:
#         label, confidence = preprocess_and_predict(image)
#         if confidence < CONFIDENCE_THRESHOLD:
#             return jsonify({'label': None, 'confidence': confidence})
#         return jsonify({'label': label, 'confidence': confidence})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/speak', methods=['POST'])
# def speak():
#     data = request.get_json()
#     if not data or 'text' not in data:
#         return jsonify({'error': 'No text provided'}), 400

#     text = data['text'].strip()
#     if not text:
#         return jsonify({'error': 'Empty text'}), 400

#     try:
#         tts = gTTS(text=text, lang='ne')
#         os.makedirs('static', exist_ok=True)
#         fname = f'static/{uuid.uuid4().hex}.mp3'
#         tts.save(fname)

#         if not os.path.exists(fname):
#             return jsonify({'error': 'Failed to create audio'}), 500

#         return send_file(fname, mimetype='audio/mpeg')
#     except Exception as e:
#         return jsonify({'error': f'TTS failed: {str(e)}'}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)