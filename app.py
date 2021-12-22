from itertools import count
from os import stat
from re import S
from flask import Flask, request, redirect, render_template, jsonify
import youtube
from threading import Thread
import time

app = Flask(__name__)

# def threaded_task():
#     print("흠...")
#     time.sleep(3)
#     print("end")
def threaded_task(url):
    print("download start")
    youtube.download(url)
    print("download end")
def threaded_start():
    print("ttttt")
    time.sleep(3)
    print("ttttt")

@app.route("/")
def main():
    print("main start")
    global url
    url=""
    # global status
    # status=1
    return render_template("main.html")

@app.route("/video")
def inputUrl():
    print("input start")
    return render_template("inputUrl.html")

@app.route("/video_download", methods=["POST"])
def video_download():
    global url
    url = request.form.get("YoutubeURL")
    print("video_download start")
    # global status
    # print("?????????")
    # print("load status :",status.is_alive())
    print("URL = [",url,"]")
    return render_template("3.html")

@app.route("/video_downloading", methods=["POST"])
def video_downloading1():
    global url
    print("제발",url,type(url))
    global status
    status = Thread(target=threaded_task(url))
    status.daemon = False
    status.start()
    # print("loading status :",status.is_alive())
    # return jsonify({
    #     "stauts":str("loading..." if status.is_alive() else " "),
    #     "alive":status.is_alive()
    # })
    # return redirect("/")
    print("is alive?",status.is_alive())
    while status.is_alive():
        time.sleep(1)
        print("now alive?")

    return jsonify({
        "alive":"alive",
        "url":url
    })

@app.route("/video_downloading/l", methods=["POST"])
def video_downloading():
    global url
    return jsonify({
        "alive":"alive",
        "url":url
    })

@app.route("/video_file/<tag>")
def video_file_download(tag):
    global url
    print(tag)
    #tag로 파일 찾아서 넘겨주기
    return render_template("loader.html")

app.run(debug=True,host="0.0.0.0",port="8000")