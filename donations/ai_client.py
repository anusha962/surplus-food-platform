import requests


def verify_food_image(image_file):
    """
    Sends the uploaded image to the local AI verification service.
    Returns a dict like {"is_food": True, "top_predictions": [...]}
    or None if the service is unreachable (fails gracefully).
    """
    try:
        image_file.seek(0)
        response = requests.post(
            "http://127.0.0.1:8001/verify-food-image/",
            files={"file": (image_file.name, image_file.read(), image_file.content_type)},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None