import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
URL = f"https://crypto-balance-notifier-bot.onrender.com/{TOKEN}"

res = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
print(res.text)

price = get_xrp_price()
if price is None:
    bot.send_message(chat_id=chat_id, text="❌ Не удалось получить цену XRP. Попробуйте позже.")
    return 'ok'
