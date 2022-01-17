import pandas as pd
import numpy as np
import spacy
import json
import random
import re
df = pd.read_csv("assignment 3\output.csv")

categories = set(df.iloc[:, 0].unique())
entity = df.iloc[:, 0]
word = df.iloc[:, 1]
count = 0

df.iloc[:, 1] = df.iloc[:, 1].fillna('--')


"""
[["",{"entities":[[<start>,<end>,<entity = "PERSON">]]}], []]

["Mr. Danywhere.", {"entities": [[0,11,"PERSON"],[166,178,"PERSON"],[394,400,"PERSON"]]}],

nan_rows = df[df.isnull().any(1)].reset_index().iloc[:, 0].to_list()
# print(nan_rows)
"""

string = ""
dataset = []
entities_for_sentence = []
for key, value in zip(entity, word):
    str_len = len(string)
    word_len = len(value)
    #print(key, " ", value, " ", str_len, " ", word_len+str_len)

    if (value == "--"):

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
"""
for sentence in dataset:
    print(sentence)
    print("\n")
"""
file = 'dataset.json'
with open(file, 'w') as f:
    json.dump(dataset, f)
