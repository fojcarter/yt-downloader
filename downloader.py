import yt_dlp

# 다운로드 옵션 정의
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',          # 고화질 + 고음질 병합
    'merge_output_format': 'mp4',                  # 결과물 mp4
    'outtmpl': '%(upload_date)s_%(title).100s.%(ext)s',  # 날짜+제목으로 저장
    'writeautomaticsub': True,                     # 자동 자막 다운로드
    'subtitleslangs': ['ko', 'en'],                # 자막 언어 우선순위
    'noplaylist': True,                            # 재생목록 무시
    'quiet': False,                                # 다운로드 상태 출력
    'no_warnings': True,
    'ignoreerrors': True,                          # 오류 무시하고 계속 진행
    'postprocessors': [{
        'key': 'FFmpegMetadata',
    }]
}

# 다운로드할 유튜브 영상 URL 목록
video_urls = [
    'https://www.youtube.com/watch?v=hLOqV8X1Oy8',
    # 여기 원하는 영상 URL 추가
    # 'https://www.youtube.com/watch?v=xxxxx',
]

# 실행
if __name__ == "__main__":
    print("🎬 유튜브 영상 다운로드 시작...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_urls)
    print("✅ 모든 작업 완료!")
