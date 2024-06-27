from locust import HttpUser, task, between
import base64

headers = {"Host": "cifar10.default.emlo.mmg", "Content-Type": "application/json"}


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def create_payload(base64_data):
    return {"instances": [{"data": base64_data}]}


encoded_image = encode_image_to_base64("dog.jpg")
payload = create_payload(encoded_image)


class StressTest(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_text_endpoint(self):
        url = "/v1/models/cifar10:predict"
        res = self.client.post(url=url, headers=headers, json=payload)
