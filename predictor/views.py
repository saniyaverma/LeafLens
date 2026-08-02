import os
import base64

from django.conf import settings
from django.shortcuts import render

from .utils import predict_image
from .disease_info import DISEASE_INFO

DISPLAY_NAMES = {
    "Tomato___Bacterial_spot": "Bacterial Spot",
    "Tomato___Early_blight": "Early Blight",
    "Tomato___Late_blight": "Late Blight",
    "Tomato___Leaf_Mold": "Leaf Mold",
    "Tomato___Septoria_leaf_spot": "Septoria Leaf Spot",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Spider Mites",
    "Tomato___Target_Spot": "Target Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomato Yellow Leaf Curl Virus",
    "Tomato___Tomato_mosaic_virus": "Tomato Mosaic Virus",
    "Tomato___healthy": "Healthy Leaf",
}


def index(request):
    return render(request, "predictor/index.html")


def predict(request):

    if request.method == "POST" and request.FILES.get("image"):

        image = request.FILES["image"]

        # -----------------------------
        # Convert uploaded image to Base64
        # -----------------------------
        image_bytes = image.read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        image_data = f"data:{image.content_type};base64,{image_base64}"

        # Reset file pointer so Django can read it again
        image.seek(0)

        # -----------------------------
        # Save temporarily for prediction
        # -----------------------------
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        image_path = os.path.join(
            settings.MEDIA_ROOT,
            image.name
        )

        with open(image_path, "wb+") as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # -----------------------------
        # AI Prediction
        # -----------------------------
        prediction, confidence = predict_image(image_path)

        display_name = DISPLAY_NAMES.get(
            prediction,
            prediction.replace("Tomato___", "").replace("_", " ").title()
        )

        info = DISEASE_INFO.get(
            prediction,
            {
                "description": "No information available.",
                "treatment": "No treatment available."
            }
        )

        context = {
            "prediction": display_name,
            "confidence": confidence,
            "description": info["description"],
            "treatment": info["treatment"],
            "image_url": image_data,
        }

        return render(
            request,
            "predictor/result.html",
            context,
        )

    return render(request, "predictor/index.html")