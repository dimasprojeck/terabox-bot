import os
import requests

def upload_file_to_terabox(link, image_path=None):
    csrf_token = os.getenv("CSRF_TOKEN")
    ndus = os.getenv("NDUS")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": f"ndus={ndus}; csrfToken={csrf_token}",
        "X-CSRF-TOKEN": csrf_token
    }

    if not image_path or not os.path.exists(image_path):
        return "⚠️ File tidak ditemukan."

    filename = os.path.basename(image_path)
    upload_url = "https://web.terabox.com/api/upload?app_id=250528"
    files = {'file': (filename, open(image_path, 'rb'))}
    data = {'rtype': '1', 'path': f'/TelegramBot/{filename}'}

    try:
        response = requests.post(upload_url, headers=headers, files=files, data=data)
        result = response.json()
        if result.get("errno") == 0:
            return f"https://www.terabox.com/web/main#dir=/TelegramBot"
        else:
            return f"❌ Upload gagal: {result.get('errmsg', 'Unknown error')}"
    except Exception as e:
        return f"❌ Terjadi error saat upload: {str(e)}"
