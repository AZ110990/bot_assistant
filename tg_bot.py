import requests
import os

# Замените 'YOUR_TOKEN' на токен вашего бота
BOT_TOKEN = os.environ.get("TOKEN_BOT")
# Замените 'CHAT_ID' на ID чата, куда вы хотите отправить сообщение
CHAT_ID = os.environ.get("MY_CHAT_ID")

def send_msg(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url).json() # Эта строка отсылает сообщение