from audioop import mul
import pandas as pd
import numpy as np
import spacy
import json
import random
import re
from spacy.training.example import Example

"""
def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)


TRAIN_DATA = load_data("assignment 3\dataset.json")


def train_spacy(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank("en")
    print(nlp.pipe_names)
    if "ner" not in nlp.pipe_names:

        ner = nlp.create_pipe("ner")
        nlp.add_pipe("ner")
        print(nlp.pipe_names)

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example],
                           drop=0.2,
                           sgd=optimizer,
                           losses=losses
                           )
            print(losses)
    return (nlp)


def clean_text(text):
    cleaned = re.sub(r"[\(\[].*?[\)\]]", "", text)
    return (cleaned)


nlp = train_spacy(TRAIN_DATA, 20)
nlp.to_disk("assignment 3\ner_model")


def training(model_name):
    with open("assignment 3\dataset.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    sentences = texts
    w2v_model = Word2Vec(min_count=5,
                         window=2,
                         size=500,
                         sample=6e-5,
                         alpha=0.03,
                         min_alpha=0.0007,
                         negative=20
                         )
"""


def test_model(test):
    """
    this function is created to test the ner model created above

    """
    nlp = spacy.load("assignment 3\ner_model")
    doc = nlp(test)
    for ent in doc.ents:
        print(ent.text, ent.label_)


test_model('resturant')
