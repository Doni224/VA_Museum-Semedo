from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, jsonify
from flask_mysqldb import MySQL, MySQLdb
from functools import wraps
from flask_cors import CORS
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
CORS(app)
#Konfigurasi Database
app.config['MYSQL_HOST'] = '45.143.81.40'
app.config['MYSQL_USER'] = ' u1547396_haisus'
app.config['MYSQL_PASSWORD'] = 'Y7,*V2I-+tpV'
app.config['MYSQL_DB'] = ' u1547396_haisus'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'virtualassisten'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)

#Konfigurasi folder menyiman dataset
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = 'pre_img/'

PATH = '\\'.join(os.path.abspath(__file__).split('\\')[0:-1])
DATASET_PATH = os.path.join(PATH, "train_img")



#-------------------- Halaman Utama ----------------

#menampilkan halaman utama
@app.route('/')
def home():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM home')
    data = cur.fetchall()
    cur.execute('SELECT * FROM about')
    dataku = cur.fetchall()
    cur.execute('SELECT * FROM kontak')
    datakon = cur.fetchall()
    cur.close()
    return render_template("index.html", home=data, kk=dataku, kontak=datakon)
  

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

# @app.route('/')
# def about():
#     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#     cur.execute('SELECT * FROM about')
#     dataku = cur.fetchall()
#     cur.close()
#     return render_template('index.html', kk = dataku)

@app.route('/koleksi1')
def koleksi1():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM koleksi')
    data = cur.fetchall()
  
    cur.close()
    return render_template('koleksi1.html', menukoleksi = data)

@app.route('/detailkoleksi/<detail_id>')
def detailkoleksi(detail_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM koleksi WHERE id= %s' , (detail_id,))
    data = cur.fetchone()
    cur.execute('SELECT * FROM koleksi ORDER BY RAND() LIMIT 2')
    dataku = cur.fetchall()
    cur.close()
    return render_template('detailkoleksi.html', detail = data, Detail= dataku)

@app.route('/daftarkoleksi/search')
def carikoleksi():
    keyword = request.args.get('query')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if keyword:
        # Lakukan pencarian dengan query yang diberikan menggunakan LIKE dan % untuk pencarian yang mirip
        cur.execute("SELECT * FROM koleksi WHERE namakoleksi LIKE %s", ("%" + keyword + "%",))
        data = cur.fetchall()
    else:
        # Jika tidak ada query, ambil semua data koleksi
        cur.execute("SELECT * FROM koleksi")
        data = cur.fetchall()

    return render_template('koleksi1.html', menukoleksi = data)

@app.route('/tentangkami')
def tentangkami():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM about')
    data = cur.fetchall()
  
    cur.close()
    return render_template('tentangkami.html', tentang = data)

#menampilkan  Profil
@app.route('/profil')
def profil():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM home')
    data = cur.fetchall()
  
    cur.close()
    return render_template('profil.html', home = data)

@app.route('/tentang')
def tentang():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM about')
    data = cur.fetchall()
  
    cur.close()
    return render_template('about.html', home = data)





if __name__ == '__main__':
    app.run(debug=True)

