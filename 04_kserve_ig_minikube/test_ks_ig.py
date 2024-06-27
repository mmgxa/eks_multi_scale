import base64
import requests
import json
import argparse


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def create_payload(base64_data):
    return {"instances": [{"data": base64_data}]}


parser = argparse.ArgumentParser(description="Process an image path.")
parser.add_argument("image_path", type=str, help="Path to the image file.")
args = parser.parse_args()

model_name = "emotion-classifier"
URL = f"http://44.242.169.141/"


encoded_image = encode_image_to_base64(args.image_path)
payload = create_payload(encoded_image)
headers = {
    "Host": "classifier.default.example.com",
    "Content-Type": "application/json",
}

response = requests.post(URL, headers=headers, json=payload)

print(response.json())
