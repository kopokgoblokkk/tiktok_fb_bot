import requests
from bs4 import BeautifulSoup

def download_tiktok(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

        session = requests.Session()
        # Kirim POST request ke ssstik endpoint
        res = session.post(
            "https://ssstik.io/abc",
            data={"id": url, "locale": "en"},
            headers=headers,
            timeout=15
        )

        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(res.text, "html.parser")

        # Simpan HTML untuk debugging
        with open("ssstik_debug.html", "w", encoding="utf-8") as f:
            f.write(res.text)

        # Cari tag link download video (tanpa watermark)
        video_tag = soup.find("a", attrs={"class": "result__btn", "target": "_blank"})
        if not video_tag:
            print("❌ Gagal ekstrak URL video dari HTML ssstik.io")
            return None

        video_url = video_tag.get("href")
        if not video_url:
            print("❌ Tidak menemukan URL video di tag <a>")
            return None

        # Unduh file video
        video_data = session.get(video_url, headers=headers, timeout=15)
        filename = "tiktok_video.mp4"
        with open(filename, "wb") as f:
            f.write(video_data.content)

        return filename

    except Exception as e:
        print(f"❌ Error saat mengunduh video dari ssstik: {e}")
        return None
