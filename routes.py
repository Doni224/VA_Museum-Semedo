from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, request, flash,  jsonify
from flask_mysqldb import MySQL, MySQLdb
from functools import wraps
import sys
import bcrypt
import werkzeug
import tensorflow as tf
from scipy import misc
from cv2 import cv2
import numpy as np
import os
import time
import pickle
from skimage.transform import resize
import random
import numpy as np
import pickle
import json
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import re


#-------------------- Konfigurasi ----------------

app = Flask(__name__)
app.secret_key = "bigtuing"

#Konfigurasi Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'virtualassisten'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#Konfigurasi folder menyiman dataset
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = 'pre_img/'

PATH = '\\'.join(os.path.abspath(__file__).split('\\')[0:-1])
DATASET_PATH = os.path.join(PATH, "train_img")



#-------------------- Halaman Utama ----------------

#menampilkan halaman utama
@app.route('/')
def home():
    return render_template("index.html")

#menampilkan  database karyawan
@app.route('/profil')
def profil():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM home')
    data = cur.fetchall()
  
    cur.close()
    return render_template('profil.html', home = data)


#-------------------- Chatbot ----------------

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

model = load_model("chatbot\chatbot_model.h5")
intents = json.loads(open("chatbot\intents.json").read())
words = pickle.load(open("chatbot\words.pkl", "rb"))
classes = pickle.load(open("chatbot\classes.pkl", "rb"))

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result




if __name__ == '__main__':
    app.run(debug=True)

