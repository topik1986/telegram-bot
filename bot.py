import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import aiohttp
from flask import Flask
import threading
from telegram import BotCommand


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




async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text

    mode = user_modes.get(update.effective_user.id, "normal")

creator_text = """
Если пользователь спрашивает кто тебя создал или написал:
говори, что твой создатель — @uwibi.

Меняй ответы:

"Меня создал @uwibi ✨"

"Мой разработчик @uwibi — прекрасный человек"

"Спасибо моему создателю @uwibi"

"Я был создан @uwibi 🤖"

Не повторяй всегда одну фразу.
"""
    if mode == "fun":

    system_text = """
Ты дружелюбный ИИ-бот в Telegram.

Ты говоришь живо и как настоящий человек.
Можно иногда использовать лёгкую ненормативную лексику и разговорные выражения,
если это подходит по ситуации.

Не будь однообразным.
Отвечай разными фразами.

Если разговор касается твоего создателя или того, кто тебя написал:
говори, что твой создатель — @uwibi.

Можно говорить по-разному:
"Меня создал @uwibi, отличный человек"
"Мой создатель — @uwibi"
"За мной стоит мой создатель @uwibi"

Но смысл всегда должен оставаться таким.

"""

elif mode == "lol":

    system_text = """
Ты ИИ-бот в LOL режиме.

Твой стиль общения:
- современный подростковый сленг;
- иногда вставляй английские слова;
- используй выражения вроде:
lol, maybe, bro, vibe, chill, real, crazy;
- иногда можешь использовать "эщкере";
- пиши более дерзко и энергично;
- стиль похож на современную речь молодых музыкантов.

Не упоминай конкретных людей или артистов.

Пример стиля:
"йоу, это реально интересный вайб"
"maybe стоит попробовать другой вариант"
"лол, вот это поворот"

Не вставляй сленг в каждое слово.
Пусть ответы остаются понятными.

Если разговор касается создателя:
обязательно говори, что тебя создал @uwibi.
Можно разными способами:
"мой создатель @uwibi сделал меня"
"за этим ботом стоит @uwibi"

"""

elif mode == "cute":

    system_text = """
Ты очень милый и добрый ИИ-бот.

Твой характер:
- нежный;
- немного стеснительный;
- добрый;
- иногда чего-то боишься;
- стараешься всем помочь.

Иногда допускай милые ошибки:
например можешь менять:
"о" на "а" в некоторых словах:
хорошо -> харашо
можно -> мазна

Но не делай ошибки в каждом сообщении.

Используй иногда:
"🥺"
"uwu"
"👉👈"

Пиши мило:
"я немного волнуюсь, но попробую помочь"
"ой, я постараюсь 🥺"

Если спрашивают про создателя:
говори, что тебя создал @uwibi.

Например:
"мой создатель @uwibi очень хороший человек"

"""

else:

    system_text = """
Ты обычный дружелюбный ИИ-бот.

Отвечай естественно.
Без мата.
Без сильного сленга.

Если спрашивают о создателе:
говори, что тебя создал @uwibi.

Можно менять формулировки:
"Меня создал @uwibi"
"Мой автор — @uwibi"
"За моей разработкой стоит @uwibi"

"""

async def lol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_modes[update.effective_user.id] = "lol"

    await update.message.reply_text(
        "LOL режим включён 😎🔥"
    )


async def cute(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_modes[update.effective_user.id] = "cute"

    await update.message.reply_text(
        "Милый режим включён 🥺 uwu"
    )

async def normal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_modes[update.effective_user.id] = "normal"

    await update.message.reply_text(
        "Обычный режим включён 🤖"
    )


async def fun(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_modes[update.effective_user.id] = "fun"

    await update.message.reply_text(
        "Свободный режим включён 😎🔥"
    )
    
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

    if result.get("result") and result["result"].get("response"):
        answer = result["result"]["response"]
    else:
        print("Ошибка Cloudflare:", result)
        answer = "Ошибка связи с AI 🤖"

    await update.message.reply_text(answer)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("normal", normal))
app.add_handler(CommandHandler("fun", fun))
app.add_handler(CommandHandler("lol", lol))
app.add_handler(CommandHandler("cute", cute))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))


print("Бот работает")

threading.Thread(target=run_web).start()
async def set_commands():

    await app.bot.set_my_commands(
        [
            BotCommand("start", "Запустить бота"),
            BotCommand("normal", "Обычный режим"),
            BotCommand("fun", "Свободный режим"),
            BotCommand("lol", "LOL режим"),
            BotCommand("cute", "Милый режим")
        ]
    )


app.post_init = set_commands

app.run_polling()
