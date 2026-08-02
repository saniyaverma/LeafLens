import os
import json
import numpy as np
import tensorflow as tf
from keras.layers import TFSMLayer
from PIL import Image

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "leaflens_savedmodel"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "model",
    "class_names.json"
)

# -----------------------------------------------------
# Load Model
# -----------------------------------------------------

print("Loading SavedModel...")

model = TFSMLayer(
    MODEL_PATH,
    call_endpoint="serve"
)

print("Model loaded successfully!")

# -----------------------------------------------------
# Load Class Names
# -----------------------------------------------------

with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

IMG_SIZE = 224

# -----------------------------------------------------
# Prediction Function
# -----------------------------------------------------

def predict_image(image_path):
    # Load image
    image = Image.open(image_path).convert("RGB")
    image = image.resize((IMG_SIZE, IMG_SIZE))

    # Preprocess
    image = np.array(image).astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)

    # Predict
    outputs = model(image)

    # GoogLeNet returns:
    # [main_output, aux1_output, aux2_output]
    predictions = outputs[0].numpy()

    # Predicted class
    predicted_index = np.argmax(predictions[0])
    predicted_class = class_names[predicted_index]

    # Confidence
    confidence = round(
        float(np.max(predictions[0])) * 100,
        2
    )

    return predicted_class, confidence