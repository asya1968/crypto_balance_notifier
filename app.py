from flask import Flask, request
import telegram
import requests
import os
from dotenv import load_dotenv
load_dotenv()  # Сначала загружаем .env

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Потом читаем переменные
bot = telegram.Bot(token=TOKEN)


XRP_AMOUNT = 1407.8907
BUY_COST = 2999.83598

app = Flask(__name__)

def get_xrp_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"
    headers = {"User-Agent": "Mozilla/5.0"}  # 👈 добавили заголовок
    response = requests.get(url, headers=headers)

    try:
        data = response.json()
    except Exception as e:
        raise Exception("Ошибка чтения JSON от Binance: " + str(e))

    if 'price' in data:
        return float(data['price'])
    else:
        raise Exception("В ответе Binance нет 'price': " + str(data))

@app.route("/", methods=["POST"])

def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id

    if update.message.text == '/balance':
        price = get_xrp_price()
        current_value = XRP_AMOUNT * price
        pnl = current_value - BUY_COST
        pnl_pct = pnl / BUY_COST * 100

        message = (
            f"💼 Баланс: {XRP_AMOUNT:.4f} XRP\n"
            f"💰 Цена XRP: {price:.4f} USDT\n"
            f"📊 Стоимость: {current_value:.2f} USDT\n"
            f"📈 PnL: {pnl:.2f} USDT ({pnl_pct:.2f}%)"
        )
        bot.send_message(chat_id=chat_id, text=message)

    return 'ok'

@app.route('/')
def home():
    return 'Бот работает!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

