from re import S
from flask import Flask, request, redirect, render_template, jsonify, send_file, send_from_directory
from threading import Thread

import os
import youtube
import time
import glob

app = Flask(__name__)

#https://ytdlp.run.goorm.io
# def threaded_task():
#     print("흠...")
#     time.sleep(3)
#     print("end")
def threaded_task(url):
    print("download start")
    a = youtube.download(url)
    print("download end")

@app.route("/")
def main():
    print("main start")
    global url
    url=""
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
    print(f"file {tag}")
    namelst = glob.glob(f"*{tag}*.mp4")+glob.glob(f"*{tag}*.webm")
    print(namelst)
    return render_template("loader.html", files=namelst[0])

@app.route("/video_files", methods=["GET","POST"])
def video_file_download2():
    global url
    #tag로 파일 찾아서 넘겨주기
    filename = request.form.get("name")
    print(filename,"제발 이거 되나..")
    return send_file("/home/sutjjang/Code/git/Daegu-Ai-Hub_last/a.csv",
    # download_name=f"new_{filename}",
    download_name=f"new.csv",
    as_attachment=True
    )
    # return redirect("/")

@app.route("/video_files/<tag>", methods=["GET","POST"])
def video_file_download3(tag):
    print(tag)
    # return redirect("/thumbnail")
    return send_file(
        # "/home/sutjjang/Code/git/Daegu-Ai-Hub_last/a.csv",
        f"./{tag}",
        # download_name=f"new.csv",
        mimetype="video/webm",
        download_name=f"{tag}",
        as_attachment=True
    )
    # return send_from_directory("./","f{tag}",as_attachment=True)
    
@app.route("/thumbnail")
def thumbnail():
    return render_template("Thumbnail.html")

app.run(debug=True,host="0.0.0.0",port="25565")