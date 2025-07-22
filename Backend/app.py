from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can access

model = load_model('digit_recognizer.h5')

@app.route('/')
def home():
    return 'Digit Recognizer Backend Running'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'No image data'}), 400

    image_data = data['image'].split(',')[1]  # Remove header like: "data:image/png;base64,..."
    image = Image.open(BytesIO(base64.b64decode(image_data))).convert('L')
    image = image.resize((28, 28))
    image = np.array(image) / 255.0
    image = image.reshape(1, 28, 28, 1)

    prediction = model.predict(image)
    digit = int(np.argmax(prediction))

    return jsonify({'prediction': digit})

if __name__ == '__main__':
    app.run(debug=True)
