import base64
import requests
import json


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def create_payload(base64_data):
    return {"instances": [{"data": base64_data}]}


model_name = "emotion-classifier"
URL = f"http://44.242.169.141/v1/models/{model_name}:predict"


encoded_image = encode_image_to_base64("img.jpg")
payload = create_payload(encoded_image)
headers = {
    "Host": f"{model_name}.default.example.com",
    "Content-Type": "application/json",
}

response = requests.post(URL, headers=headers, json=payload)

print(response.json())
