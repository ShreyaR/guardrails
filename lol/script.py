# script.py
import subprocess
import sys

# Install all required packages
subprocess.check_call(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
)

import ray
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
import torch
from nli_fine_tuning import main_function

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
model_name = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-docnli-ling-2c"
print(f"Device: {device}")


@ray.remote
def driver():
    return main_function(model_name)


ray.init()
print(
    """This cluster consists of {} nodes\n{} CPU resources\n{} GPU resources""".format(
        len(ray.nodes()), ray.cluster_resources()["CPU"], ray.cluster_resources()["GPU"]
    )
)

path = ray.get(driver.remote())
print("The path to the saved model is {}".format(path))

# Load saved model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(path)

premise = "I first thought that I liked the movie, but upon second thought it was actually disappointing."
hypothesis = "The movie was good."

input = tokenizer(
    premise,
    hypothesis,
    padding="max_length",
    return_token_type_ids=True,
    truncation=True,
    return_tensors="pt",
)
output = model(input["input_ids"])  # device = "cuda:0" or "cpu"
prediction = torch.softmax(output["logits"][0], -1).tolist()
label_names = ["entailment", "not_entailment"]
prediction = {
    name: round(float(pred) * 100, 1) for pred, name in zip(prediction, label_names)
}
print(prediction)
