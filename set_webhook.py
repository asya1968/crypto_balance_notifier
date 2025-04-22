import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://crypto-balance-notifier-bot.onrender.com/{TOKEN}"

res = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
print(res.text)
