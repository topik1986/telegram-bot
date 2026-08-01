import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import aiohttp
from flask import Flask
import threading



TOKEN = os.getenv("TELEGRAM_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_TOKEN = os.getenv("CF_TOKEN")

web_app = Flask(__name__)

@web_app.route("/")

def home():

    return "Bot is running"

def run_web():

    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
user_modes = {}




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши мне сообщение 🤖"
    )
async def normal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_modes[update.effective_user.id] = "normal"
    await update.message.reply_text(
        "Включён обычный режим 🤖"
    )


async def fun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_modes[update.effective_user.id] = "fun"
    await update.message.reply_text(
        "Включён свободный режим 😎"
    )
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    mode = user_modes.get(update.effective_user.id, "normal")



    if mode == "fun":
        system_text = """
        Ты дружелюбный ИИ-бот в Telegram.
        Отвечай живо и разнообразно.
        Не повторяй одинаковые фразы.
        Можешь иногда использовать лёгкую нецензурную брань, если это подходит по ситуации.
        Общайся как настоящий собеседник.
        Не оскорбляй людей сликшом грубо.
        """
    else:
        system_text = """
        Ты дружелюбный ИИ-бот в Telegram.
        Отвечай живо, интересно и разнообразно.
        Не используй одинаковые заготовленные ответы.
        Общайся естественно, как человек.
        Отвечай культурно, без мата.
        """

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct"

    headers = {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": system_text
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

print("ОТПРАВЛЯЮ В CLOUDFLARE")
print("ACCOUNT:", CF_ACCOUNT_ID)
print("TOKEN ЕСТЬ:", bool(CF_TOKEN))

async with aiohttp.ClientSession() as session:
    async with session.post(url, headers=headers, json=data) as r:
        result = await r.json()
        print("ОТВЕТ CLOUDFLARE:", result)
        
 if result.get("result") and "response" in result["result"]:
     answer = result["result"]["response"]
else:
     print("Ошибка Cloudflare:", result)
     answer = "Ошибка связи с AI 🤖"
        
await update.message.reply_text(answer)



app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("normal", normal))
app.add_handler(CommandHandler("fun", fun))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))


print("Бот работает")

threading.Thread(target=run_web).start()
app.run_polling()
