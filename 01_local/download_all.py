from transformers import AutoImageProcessor, AutoModelForImageClassification


def get_processor_and_model(hf_string):
    processor = AutoImageProcessor.from_pretrained(hf_string)
    model = AutoModelForImageClassification.from_pretrained(hf_string)

    return [processor, model]


def save_model_processor(model, processor, save_prefix_str):
    model.save_pretrained(f"../models/{save_prefix_str}/model")
    processor.save_pretrained(f"../models/{save_prefix_str}/processor")


HF_MODELS = [
    {"name": "nateraw/vit-base-patch16-224-cifar10", "destination": "cifar10"},
    {"name": "Sena/dog", "destination": "dog-classifier"},
    {
        "name": "dima806/man_woman_face_image_detection",
        "destination": "gender-classifier",
    },
    {"name": "dima806/faces_age_detection", "destination": "age-classifier"},
    {"name": "PriyamSheta/EmotionClassModel", "destination": "emotion-classifier"},
]

for hf_model in HF_MODELS:
    [processor, model] = get_processor_and_model(hf_model["name"])
    save_model_processor(model, processor, hf_model["destination"])
