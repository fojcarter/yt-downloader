from flask import Flask, render_template, request
from datetime import datetime
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        url = request.form.get("url")
        resolution = request.form.get("resolution")
        include_subs = request.form.get("subtitles") == "true"

        if url:
            try:
                format_str = 'bestvideo+bestaudio/best'
                if resolution == "1080p":
                    format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                elif resolution == "4k":
                    format_str = 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'

                ydl_opts = {
                    'format': format_str,
                    'merge_output_format': 'mp4',
                    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(upload_date)s_%(title).80s.%(ext)s'),
                    'quiet': True,
                    'ignoreerrors': True,
                    'noplaylist': True,
                    'postprocessors': [{'key': 'FFmpegMetadata'}]
                }

                if include_subs:
                    ydl_opts.update({
                        'writesubtitles': True,
                        'writeautomaticsub': True,
                        'subtitleslangs': ['ko', 'en']
                    })

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 출처 정보 저장
                with open(os.path.join(DOWNLOAD_DIR, "출처.txt"), "w", encoding="utf-8") as f:
                    f.write(f"원본 영상: {url}\n다운로드 날짜: {datetime.now()}\n")

                message = "✅ 다운로드 완료!"
            except Exception as e:
                message = f"❌ 오류 발생: {str(e)}"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
