from flask import Flask, request, redirect, render_template, jsonify, send_file, send_from_directory
from threading import Thread

import os
import youtube
import time
import glob
import re

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

#video download main page
@app.route("/video")
def inputUrl():
    print("input start")
    return render_template("inputUrl.html")

#downloading page(다운로드 전 준비 화면, 섬네일 보여주며 확인 하고 다운 로드 진행 전 url 중복으로 입력 되는 것을 막기 위한 장치)
@app.route("/video_download", methods=["POST"])
def video_download():
    print("video_download start")
    # global url
    url = request.form.get("YoutubeURL")
    yt_pattern = "(http|https):\/\/(youtu.be\/|www.youtube.com\/watch\?v=)"
    tag = re.sub(yt_pattern,"",url)
    print("URL = [",url,"]")
    print("tag = [",tag,"]")
    return render_template("3.html", tag=f"{tag}")

#downloading backend
@app.route("/video_downloading", methods=["POST"])
def video_downloading1():
    print("now video downloading... is loading")
    tag = request.form["tag"]
    url = "https://youtu.be/"+tag
    status = Thread(target=threaded_task(url))
    status.daemon = False
    status.start()
    print("is alive?",status.is_alive())
    while status.is_alive():
        time.sleep(1)
        print("now alive?")

    return jsonify({
        # "alive":"alive",
        "url":url,
        "tag":tag
    })

#search video file
@app.route("/video_file/<tag>")
def video_file_download(tag):
    global url
    print(tag)
    #tag로 파일 찾아서 넘겨주기
    print(f"file {tag}")
    namelst = glob.glob(f"download/{tag}*.mp4")+glob.glob(f"download/{tag}*.webm")
    print(namelst[0][9:])
    return render_template("loader.html", files=namelst[0][9:])

#send video file
@app.route("/video_files/<name>", methods=["GET","POST"])
def video_file_download3(name):
    print("send file :",name)
    # return redirect("/thumbnail")
    return send_file(
        f"download/{name}",
        # download_name=f"new.csv", 저장시 파일명 설정 필요할 경우
        mimetype="video/webm",
        download_name=f"{name}",
        as_attachment=True
    )
    # return send_from_directory("./","f{tag}",as_attachment=True)
    
@app.route("/thumbnail")
def thumbnail():
    return render_template("Thumbnail.html")

app.run(debug=True,host="0.0.0.0",port="8000")