from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import io

from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2, preprocess_input, decode_predictions
)

app = FastAPI()

# Allow requests from your Django backend / frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading MobileNetV2 model... (this happens once, on startup)")
model = MobileNetV2(weights="imagenet")
print("Model loaded.")

# A rough set of ImageNet class names that indicate "food-like" content.
# MobileNetV2 was trained on 1000 general categories, not specifically
# food — but a decent number of its classes are food items, so we treat
# any top prediction from this set as a food signal.
FOOD_KEYWORDS = [
    "pizza", "hamburger", "hotdog", "ice_cream", "bagel", "pretzel",
    "burrito", "guacamole", "carbonara", "trifle", "consomme",
    "plate", "cup", "wine", "banana", "orange", "strawberry", "broccoli",
    "cucumber", "mushroom", "corn", "meat_loaf", "potpie", "pomegranate",
    "cheeseburger", "french_loaf", "custard", "espresso", "chocolate",
    "sandwich",
]


@app.get("/")
def health_check():
    return {"status": "AI verification service is running"}


@app.post("/verify-food-image/")
async def verify_food_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((224, 224))

    arr = np.array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)

    predictions = model.predict(arr, verbose=0)
    decoded = decode_predictions(predictions, top=5)[0]
    # decoded is a list of (class_id, class_name, confidence)

    top_labels = [(label, float(conf)) for (_, label, conf) in decoded]
    is_food = any(
        any(keyword in label.lower() for keyword in FOOD_KEYWORDS)
        for label, _ in top_labels
    )

    return {
        "is_food": is_food,
        "top_predictions": [
            {"label": label, "confidence": round(conf, 4)} for label, conf in top_labels
        ],
    }