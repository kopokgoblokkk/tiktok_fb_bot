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
        res_get = session.get("https://ssstik.io/en", headers=headers, timeout=10)
        soup_get = BeautifulSoup(res_get.text, "html.parser")

        # Ambil token dari input hidden
        token = soup_get.find("input", {"id": "token"})
        if not token:
            print("❌ Token tidak ditemukan, halaman dilindungi Cloudflare?")
            return None

        token_value = token.get("value")

        res_post = session.post(
            "https://ssstik.io/abc",
            data={"id": url, "locale": "en", "token": token_value},
            headers=headers,
            timeout=15
        )

        soup_post = BeautifulSoup(res_post.text, "html.parser")

        # Simpan debug HTML
        with open("ssstik_debug.html", "w", encoding="utf-8") as f:
            f.write(res_post.text)

        # Cari URL unduhan
        a_tag = soup_post.find("a", href=True, attrs={"class": "result__btn", "target": "_blank"})
        if not a_tag:
            print("❌ Gagal menemukan tag download di HTML.")
            return None

        video_url = a_tag["href"]
        video_res = session.get(video_url, headers=headers)

        with open("tiktok_video.mp4", "wb") as f:
            f.write(video_res.content)

        return "tiktok_video.mp4"

    except Exception as e:
        print(f"❌ Error saat unduh TikTok: {e}")
        return None
