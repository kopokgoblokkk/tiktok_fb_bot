import requests
from bs4 import BeautifulSoup
import time

def download_tiktok(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://ttdownloader.com/"
        }

        session = requests.Session()

        # 1. Buka halaman awal untuk ambil cookie dan token
        home_page = session.get("https://ttdownloader.com/", headers=headers)
        soup = BeautifulSoup(home_page.text, "html.parser")

        token = soup.find("input", {"id": "token"}).get("value")
        if not token:
            print("❌ Token tidak ditemukan di halaman ttdownloader.com")
            return None

        # 2. Kirim POST request untuk memproses link
        data = {
            "url": url,
            "format": "",
            "token": token
        }

        time.sleep(1.5)  # delay supaya tidak dianggap bot
        res = session.post("https://ttdownloader.com/req/", headers=headers, data=data)
        soup = BeautifulSoup(res.text, "html.parser")

        # 3. Ambil URL video tanpa watermark
        video_no_wm = soup.find("a", {"id": "download"}).get("href")

        if not video_no_wm:
            print("❌ Gagal mendapatkan URL video dari ttdownloader.com")
            return None

        # 4. Unduh video
        video_data = session.get(video_no_wm, headers=headers)
        filename = "tiktok_video.mp4"
        with open(filename, "wb") as f:
            f.write(video_data.content)

        return filename

    except Exception as e:
        print(f"❌ Error saat mengunduh dari ttdownloader: {e}")
        return None
