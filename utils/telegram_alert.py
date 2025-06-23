import requests

def send_telegram_alert(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Telegram alert failed: {response.text}")
        return response.status_code
    except Exception as e:
        print(f"Telegram exception: {e}")
        return None

def send_csv_document(file_path, bot_token, chat_id, caption="📎 Anomaly log attached"):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    try:
        with open(file_path, "rb") as file:
            files = {"document": file}
            data = {"chat_id": chat_id, "caption": caption}
            response = requests.post(url, data=data, files=files)
        if response.status_code != 200:
            print(f"Document upload failed: {response.text}")
        return response.status_code
    except Exception as e:
        print(f"Telegram document error: {e}")
        return None