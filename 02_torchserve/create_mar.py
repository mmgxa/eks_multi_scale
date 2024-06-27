import os
import subprocess
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

CONFIG_TEMPLATE = """
inference_address=http://0.0.0.0:8085
management_address=http://0.0.0.0:8085
metrics_address=http://0.0.0.0:8082
grpc_inference_port=7070
grpc_management_port=7071
enable_envvars_config=true
install_py_dep_per_model=true
load_models=all
max_response_size=655350000
model_store=/mnt/models/model-store
default_response_timeout=600
enable_metrics_api=true
metrics_format=prometheus
number_of_netty_threads=4
job_queue_size=10
model_snapshot={{"name":"startup.cfg","modelCount":1,"models":{{"{0}":{{"1.0":{{"defaultVersion":true,"marName":"{0}.mar","minWorkers":1,"maxWorkers":1,"batchSize":1,"maxBatchDelay":100,"responseTimeout":600}}}}}}}}
"""

HF_MODELS = [
    "cifar10",
    "dog-classifier",
    "gender-classifier",
    "age-classifier",
    "emotion-classifier",
]


def create_folder_structure(root, model):
    model_dir = os.path.join(root, model)
    config_dir = os.path.join(model_dir, "config")
    model_store_dir = os.path.join(model_dir, "model-store")

    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(model_store_dir, exist_ok=True)

    logger.info(f"🐎 Created folder structure for {model}")
    return model_dir


def create_config_file(model_dir, model):
    config_file = os.path.join(model_dir, "config", "config.properties")
    with open(config_file, "w") as file:
        file.write(CONFIG_TEMPLATE.format(model))
    logger.info(f"📂 Created config.properties for {model}")


def create_mar_file(model, model_store_dir):
    cmd = [
        "torch-model-archiver",
        "--model-name",
        model,
        "--handler",
        "hf_image_classification_handler.py",
        "--extra-files",
        f"../models/{model}/",
        "--version",
        "1.0",
        "--export-path",
        model_store_dir,
    ]
    try:
        logger.info(f"🏃 Creating {model}.mar in {model_store_dir}")
        subprocess.check_call(cmd)
        logger.info(f"🪄  Created {model}.mar in {model_store_dir}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create {model}.mar", exc_info=True)


if __name__ == "__main__":
    root = "../model-store"
    for model in HF_MODELS:
        model_dir = create_folder_structure(root, model)
        create_config_file(model_dir, model)
        create_mar_file(model, os.path.join(model_dir, "model-store"))
        logger.info(f" 🎉🎉 Finished processing model {model} ")
