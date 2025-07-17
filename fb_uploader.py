import requests
from config import FB_PAGE_ID, FB_ACCESS_TOKEN

def upload_to_facebook(video_path):
    url = f"https://graph-video.facebook.com/v19.0/{FB_PAGE_ID}/videos"
    files = {'source': open(video_path, 'rb')}
    data = {
        'access_token': FB_ACCESS_TOKEN,
        'title': 'Video TikTok',
        'description': 'Diunggah otomatis dari bot Telegram.'
    }
    response = requests.post(url, files=files, data=data)
    return response.json()
