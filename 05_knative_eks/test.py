import argparse
import base64
import requests
import json


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def create_payload(base64_data):
    return {"instances": [{"data": base64_data}]}


def send_request(
    model_name, image_path, external_host, service_hostname, isvc_name, is_ig=False
):
    encoded_image = encode_image_to_base64(image_path)
    payload = create_payload(encoded_image)
    headers = {"Host": service_hostname, "Content-Type": "application/json"}
    url = (
        f"http://{external_host}/v1/models/{model_name}:predict"
        if not is_ig
        else f"http://{external_host}/"
    )

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


parser = argparse.ArgumentParser(description="Process an image path.")
parser.add_argument("image_path", type=str, help="Path to the image file.")
args = parser.parse_args()

MODEL_NAME = "cifar10"
ISVC_NAME = "cifar10"
IS_IG = False
EXTERNAL_HOST = "a771550c1fe3f4dd78478c382f854b28-610241996.us-west-2.elb.amazonaws.com"
SERVICE_HOSTNAME = f"{ISVC_NAME}.default.emlo.mmg"

response = send_request(
    MODEL_NAME, args.image_path, EXTERNAL_HOST, SERVICE_HOSTNAME, IS_IG
)

print(json.dumps(response, indent=2, ensure_ascii=False))
