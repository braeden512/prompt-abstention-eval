import os
import json
import random
from datasets import load_dataset
# import constants from config file
from config import SAMPLE_PER_SPLIT, RANDOM_SEED

# returns two lists of dicts for answerable and unanswerable questions, each dict has keys id, question, context, answers, and is_answerable
def load_squad2(sample_per_split=SAMPLE_PER_SPLIT, seed=RANDOM_SEED):

    print("Downloading SQuAD2.0 from HuggingFace...")
    # use validation split which has both answerable and unanswerable questions
    dataset = load_dataset("squad_v2", split="validation")

    answerable = []
    unanswerable = []

    for item in dataset:
        # unanswerable questions have an empty answers dict
        is_answerable = len(item["answers"]["text"]) > 0
        record = {
            "id": item["id"],
            "question": item["question"],
            "context": item["context"],
            "answers": item["answers"]["text"],
            "is_answerable": is_answerable,
        }
        if is_answerable:
            answerable.append(record)
        else:
            unanswerable.append(record)

    # print stats
    print(f"Total answerable: {len(answerable)}, unanswerable: {len(unanswerable)}")

    # sample part of the dataset, with a fixed random seed for reproducibility
    random.seed(seed)
    if sample_per_split and sample_per_split < len(answerable):
        answerable = random.sample(answerable, sample_per_split)
    if sample_per_split and sample_per_split < len(unanswerable):
        unanswerable = random.sample(unanswerable, sample_per_split)

    # print stats after sampling
    print(f"Sampled: {len(answerable)} answerable, {len(unanswerable)} unanswerable")

    return answerable, unanswerable