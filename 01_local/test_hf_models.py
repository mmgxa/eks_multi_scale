from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import requests
import torch

HF_MODELS = [
    "cifar10",
    "dog-classifier",
    "gender-classifier",
    "age-classifier",
    "emotion-classifier",
]
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)


def do_classification(model, images, processor):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits
    # Apply softmax to convert logits into probabilities
    probabilities = torch.softmax(logits, dim=-1)

    # Get the top-1 class index and its probability
    predicted_class_idx = probabilities.argmax(-1).item()
    predicted_prob = probabilities.max(-1).values.item()

    # Get the class label using the index
    predicted_class_label = model.config.id2label[predicted_class_idx]

    print(f"Predicted class: {predicted_class_label}, Probability: {predicted_prob}")


for model_name in HF_MODELS:
    print(f"Loading model: {model_name}")
    processor = AutoImageProcessor.from_pretrained(f"../models/{model_name}/processor")
    model = AutoModelForImageClassification.from_pretrained(
        f"../models/{model_name}/model"
    )
    do_classification(model, image, processor)
