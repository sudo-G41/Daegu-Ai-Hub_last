from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def index():
    f = open("index.html","r")
    page = f.read()
    return page

@app.route("/h")
def h():
    f = open("1.html","r")
    page = f.read()
    return page

@app.route("/c")
def c():
    f = open("2.html","r")
    page = f.read()
    # os.system("yt-dlp -F https://youtu.be/0kIMgvotSgM")
    return page

app.run(debug=True,host="0.0.0.0",port="8000")
