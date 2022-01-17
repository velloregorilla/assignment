from audioop import mul
import pandas as pd
import numpy as np
import spacy
import json
import random
import re
from spacy.training.example import Example

"""

df = pd.read_csv("assignment 3\output.csv")

categories = set(df.iloc[:, 0].unique())
entity = df.iloc[:, 0]
word = df.iloc[:, 1]
count = 0

df.iloc[:, 1] = df.iloc[:, 1].fillna('--')
### NaN with --


### dataset format [["",{"entities":[[<start>,<end>,<entity = "PERSON">]]}], []]


###nan_rows = df[df.isnull().any(1)].reset_index().iloc[:, 0].to_list()
# print(nan_rows)

### the below code creates dataset from csv file
string = ""
dataset = []
entities_for_sentence = []
for key, value in zip(entity, word):
    str_len = len(string)
    word_len = len(value)
    #print(key, " ", value, " ", str_len, " ", word_len+str_len)

    if (value == "--"):
        ## if value is -- it means the sentence is over
        ## enter the complete data into the format mentioned above
        entities = {"entities": entities_for_sentence}
        sentences = []
        sentences.append(string)
        sentences.append(entities)
        dataset.append(sentences)
        entities_for_sentence = []
        string = ""

    else:
        string = string + value + " "
        temp = []
        temp.append(str_len)
        temp.append(word_len+str_len)
        temp.append(key)
        entities_for_sentence.append(temp)

    count = count+1

file = 'dataset.json'
with open(file, 'w') as f:
    json.dump(dataset, f)
### json dataset created


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)


TRAIN_DATA = load_data("assignment 3\dataset.json")


def train_spacy(data, iterations):
    ### this function creates models from the dataset created
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

nlp = train_spacy(TRAIN_DATA, 20)
nlp.to_disk("assignment 3\ner_model")

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
