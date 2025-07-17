import requests
import re

def download_tiktok(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "id": url,
            "locale": "en",
            "tt": "MT=="
        }

        res = requests.post("https://ssstik.io/abc?url=dl", headers=headers, data=data)
        if res.status_code != 200:
            print("❌ Gagal request ke ssstik.io")
            return None

        # Ekstrak URL video tanpa watermark
        video_url = re.search(r'href=\"(https://[^"]+\.mp4)\"', res.text)
        if not video_url:
            print("❌ Gagal ekstrak URL video dari HTML ssstik.io")
            return None

        video_link = video_url.group(1)
        video_data = requests.get(video_link)
        if video_data.status_code != 200:
            print("❌ Gagal unduh video dari URL yang ditemukan")
            return None

        with open("tiktok_video.mp4", "wb") as f:
            f.write(video_data.content)

        return "tiktok_video.mp4"

    except Exception as e:
        print(f"❌ Error download_tiktok: {e}")
        return None
