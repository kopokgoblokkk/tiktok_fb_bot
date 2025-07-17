import requests

def download_tiktok(url):
    try:
        api = f"https://tikcdn.io/api/download?url={url}"
        res = requests.get(api)
        data = res.json()
        video_url = data['video']

        video_file = "tiktok_video.mp4"
        video_data = requests.get(video_url)
        with open(video_file, "wb") as f:
            f.write(video_data.content)
        return video_file
    except Exception as e:
        print(f"Error: {e}")
        return None
