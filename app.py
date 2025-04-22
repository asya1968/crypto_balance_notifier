from flask import Flask, request
import telegram
import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

XRP_AMOUNT = 1407.8907
BUY_COST = 2999.83598

app = Flask(__name__)

def get_xrp_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"
    data = requests.get(url).json()
    return data['ripple']['usd']

@app.route("/", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message is None:
        return 'ok'

    chat_id = update.message.chat.id

    if update.message.text == '/balance':
        price = get_xrp_price()
        current_value = XRP_AMOUNT * price
        pnl = current_value - BUY_COST
        pnl_pct = pnl / BUY_COST * 100

        message = (
            f"💼 Баланс: {XRP_AMOUNT:.4f} XRP\n"
            f"📉 Цена XRP: {price:.4f} USD\n"
            f"💰 Стоимость: {current_value:.2f} USD\n"
            f"📈 PnL: {pnl:.2f} USD ({pnl_pct:.2f}%)"
        )

        bot.send_message(chat_id=chat_id, text=message)
