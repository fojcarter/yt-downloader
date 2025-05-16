from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    video_file = None

    if request.method == "POST":
        url = request.form.get("url")
        quality = request.form.get("quality")
        subtitles = request.form.get("subtitles") == "on"

        ydl_opts = {
            'format': {
                '4k': 'bestvideo[height<=2160]+bestaudio/best',
                '1440p': 'bestvideo[height<=1440]+bestaudio/best',
                '1080p': 'bestvideo[height<=1080]+bestaudio/best',
                '720p': 'bestvideo[height<=720]+bestaudio/best',
                '480p': 'bestvideo[height<=480]+bestaudio/best',
                'audio': 'bestaudio/best',
                'auto': 'bestvideo+bestaudio/best'
            }.get(quality, 'bestvideo+bestaudio/best'),
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(upload_date)s_%(title).80s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'ignoreerrors': True,
            'postprocessors': [{'key': 'FFmpegMetadata'}]
        }

        if subtitles:
            ydl_opts['writeautomaticsub'] = True
            ydl_opts['subtitleslangs'] = ['ko', 'en']

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", ".mp4")
                video_file = os.path.basename(filename)
                message = "✅ 다운로드 완료!"
        except Exception as e:
            message = f"❌ 오류 발생: {str(e)}"

    return render_template("index.html", message=message, video_file=video_file)

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
