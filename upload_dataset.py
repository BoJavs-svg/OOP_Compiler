
from datasets import Dataset
from huggingface_hub import HfApi
import os
import json

jsonl_path = "valid_oop_cases.jsonl"
data = []

with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))

dataset = Dataset.from_list(data)

print(dataset)

dataset.push_to_hub("BoJavs/Clean_SweBench", token="")
