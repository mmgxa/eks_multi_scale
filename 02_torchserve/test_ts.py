import requests

url = "http://localhost:8085/predictions/cifar10"
files = {"data": open("img.jpg", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    print("Prediction successful")
    print(response.json())  # Assuming the response is in JSON format
else:
    print("Prediction failed with status code:", response.status_code)
