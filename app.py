from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'SuperSecureKey123!@#'  # ⚠️ 배포 시 더 복잡하게!
PASSWORD = "Cckkddk8^^"

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw = request.form.get("password")
        if pw == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="❌ 비밀번호가 틀렸습니다.")
    return render_template("login.html")

@app.route("/download", methods=["GET", "POST"])
def index():
    if not session.get('authenticated'):
        return redirect(url_for("login"))

    message = ""
    if request.method == "POST":
        url = request.form.get("url")
        quality = request.form.get("quality")
        subtitles = request.form.get("subtitles") == "true"

        if url:
            try:
                format_str = 'bestvideo+bestaudio/best'
                if quality == "1080p":
                    format_str = 'bestvideo[height<=1080]+bestaudio/best'
                elif quality == "4k":
                    format_str = 'bestvideo[height<=2160]+bestaudio/best'

                ydl_opts = {
                    'format': format_str,
                    'merge_output_format': 'mp4',
                    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(upload_date)s_%(title).80s.%(ext)s'),
                    'noplaylist': True,
                    'quiet': True,
                    'ignoreerrors': True,
                    'postprocessors': [{'key': 'FFmpegMetadata'}],
                }

                if subtitles:
                    ydl_opts['writeautomaticsub'] = True
                    ydl_opts['subtitleslangs'] = ['ko', 'en']

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                with open(os.path.join(DOWNLOAD_DIR, "출처.txt"), "w", encoding="utf-8") as f:
                    f.write(f"원본 영상: {url}\n다운로드 날짜: {datetime.now()}\n")

                message = "✅ 다운로드 완료!"
            except Exception as e:
                message = f"❌ 오류 발생: {str(e)}"

    return render_template("index.html", message=message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
