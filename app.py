from itertools import count
from flask import Flask, request, redirect, render_template, jsonify
import test3
from threading import Thread
import time

app = Flask(__name__)

def threaded_task():
    print("흠...")
    time.sleep(3)
    print("end")

@app.route("/")
def main():
    print("main start")
    return render_template("main.html")

@app.route("/video")
def inputUrl():
    print("input start")
    return render_template("inputUrl.html")

@app.route("/video_download", methods=["POST"])
def video_download():
    url = request.form.get("YoutubeURL")
    print("video_download start")
    global status
    status = Thread(target=threaded_task)
    status.daemon = False
    status.start()
    print("URL = [",url,"]")
    print("load status :",status.is_alive())
    return render_template("3.html")

@app.route("/video_downloading", methods=["POST"])
def video_downloading():
    global status
    print("loading status :",status.is_alive())
    return jsonify({
        "stauts":str("loading..." if status.is_alive() else " "),
        "alive":status.is_alive()
    })

@app.route("/t")
def video():
    f = open("2.html","r")
    page = f.read()
    return page

app.run(debug=True,host="0.0.0.0",port="8000")