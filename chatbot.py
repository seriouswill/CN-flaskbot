import random
import json
import pickle
import numpy as np 
from time import sleep

import pandas as pd

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model
# DATE TESTING
import datetime
date = datetime.datetime.now()

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('./intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.model')

# csv tester for teamBrians

with open("./data/Highest Holywood Grossing Movies.csv") as file:
    data = pd.read_csv(file)

film_list = {"Title": [], "Genre": []}

for x in data:
    for i in data.Title:
        film_list['Title'].append(i)
    for j in data.Genre:
        film_list['Genre'].append(j)

# print(film_list['Genre'])

def clean_up_sentance(sentance):
    sentance_words = word_tokenize(sentance)
    sentance_words = [
        lemmatizer.lemmatize(word) for word in sentance_words
        ]
    return sentance_words

def bag_of_words(sentance):
    sentance_words = clean_up_sentance(sentance)
    bag = [0] * len(words)
    for w in sentance_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentance):
    bow = bag_of_words(sentance)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r, in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({
            'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            if tag == "time":
                result = (f"It is currently {date.strftime('%T')}, on {date.strftime('%D')}, which just happens to be a {date.strftime('%A')}") + " \n " + random.choice(i['responses'])
                return result
                break
            elif tag == "codenation":
                result = random.choice(i['responses'])
                return result
                break
            elif tag == "contact":
                result = random.choice(i['responses']) 
                return result
                break
            elif tag == "courses":
                result = random.choice(i['responses'])
                return result
                break
            result = random.choice(i['responses'])
            break
    return result


print("WILLBOT3000 IS RUNNING. \n \n Ask your questions, pathetic human. ~~> :\n")

# while True:
#     message = input("")
#     if message == "quit" or message == "q":
#         print("You have chosen to quit. Good riddance.")
#         break
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     sleep(random.random())
#     print(res)
    
