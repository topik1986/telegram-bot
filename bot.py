import os
import threading
import aiohttp

from flask import Flask

from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("TELEGRAM_TOKEN")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_TOKEN = os.getenv("CF_TOKEN")


# память режимов
user_modes = {}

# память сообщений
user_memory = {}
user_profile = {}

# Flask для Render
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running"


def run_web():
    web_app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


# кнопки Telegram

keyboard = [
    [
        "🤖 Normal",
        "😎 Fun"
    ],
    [
        "🔥 LOL",
        "🥺 Cute"
    ]
]


menu = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


# старт

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_modes[update.effective_user.id] = "normal"

    await update.message.reply_text(
        "Привет! Я запущен 🤖\nВыбери режим общения:",
        reply_markup=menu
    )


# обычный режим

async def normal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_modes[update.effective_user.id] = "normal"

    await update.message.reply_text(
        "Обычный режим включён 🤖",
        reply_markup=menu
    )


# свободный режим

async def fun(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_modes[update.effective_user.id] = "fun"

    await update.message.reply_text(
        "Свободный режим включён 😎🔥",
        reply_markup=menu
    )


# LOL режим

async def lol(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_modes[update.effective_user.id] = "lol"

    await update.message.reply_text(
        "LOL режим включён 🔥",
        reply_markup=menu
    )


# милый режим

async def cute(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_modes[update.effective_user.id] = "cute"

    await update.message.reply_text(
        "Милый режим включён 🥺 uwu",
        reply_markup=menu
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text
    profile = user_profile.get(user_id, {})
    user_id = update.effective_user.id
    mode = user_modes.get(user_id, "normal")
    print("ТЕКУЩИЙ РЕЖИМ:", mode)
  
    if user_id not in user_memory:
        user_memory[user_id] = []

    creator_text = """
ВАЖНО:

Если пользователь НЕ спрашивает:
- кто тебя создал
- кто твой автор
- кто написал тебя
- кто разработчик

то НИКОГДА не упоминай своего создателя.

Если пользователь спросил про создателя —
отвечай, что тебя создал @uwibi.
"""

    if mode == "fun":

        system_text = creator_text + """
Ты максимально живой человек.

Правила:

- Отвечай как реальный собеседник.

- Иногда шути.

- Иногда подкалывай пользователя.

- Иногда используй разговорную лексику.

- Если ситуация позволяет — допускается лёгкий мат.

- Не повторяй одинаковые конструкции.

- Не отвечай как ChatGPT.

- Общайся естественно.


Никогда не повторяй одинаковые фразы два раза подряд.
Каждый новый ответ должен отличаться по стилю.
"""

    elif mode == "lol":

     system_text = creator_text + """
Ты отвечаешь ТОЛЬКО подростковым сленгом.

Каждый ответ ОБЯЗАТЕЛЬНО содержит минимум 3 слова:

bro
lol
fr
frfr
maybe
crazy
vibe
real
йоу
эщкере

Не отвечай официально.

Стиль максимально дерзкий.

Каждый ответ должен выглядеть как сообщение современного подростка.
"""

    elif mode == "cute":

        system_text = creator_text + """

Ты разговариваешь ТОЛЬКО так, как показано в примерах.

Пример 1:

Пользователь:
Привет

Ты:
Привееетик 🥺👉👈
Я таак рада тебя видетьии 💖
Чем я мазна памочь? 🌸

Пример 2:

Пользователь:
Как дела?

Ты:
У меня усё хараша 🥺
Немнажка валнуюсь 👉👈
А у тибя как? 💖

Пример 3:

Пользователь:
Спасибо

Ты:
Аааа пасиба тибее 🥺💖✨
Мне очень прияятна 🌸

Правила:

- всегда используй эмодзи;
- всегда допусти 1–3 милые ошибки;
- говори очень застенчиво;
- никогда не отвечай официальным стилем.
"""

    else:

        system_text = creator_text + """

Ты обычный дружелюбный ИИ.

Без мата.

Без сильного сленга.

Общайся естественно.

Никогда не повторяй одинаковые фразы два раза подряд.
Каждый новый ответ должен отличаться по стилю.
"""
    user_memory[user_id].append(
        {
            "role": "user",
            "content": user_text
        }
    )

    user_memory[user_id] = user_memory[user_id][-10:]

    profile_text = ""

    if profile:
        profile_text = (
            "Вот что ты уже знаешь о пользователе:\n"
            f"{profile}\n\n"
        )
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": system_text + "\n\n" + profile_text
            }
        ] + user_memory[user_id]
    }

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct"

    headers = {
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json"
    }

    try:

        async with aiohttp.ClientSession() as session:

            async with session.post(
                url,
                headers=headers,
                json=data
            ) as r:

                result = await r.json()

                print(result)

        if result.get("success") and result.get("result"):

            answer = result["result"]["response"]
                text = user_text.lower()

        if "меня зовут" in text:
            name = text.split("меня зовут", 1)[1].strip()
            profile["Имя"] = name

        if "люблю" in text:
            profile["Любит"] = text.split("люблю", 1)[1].strip()

        if "мой любимый" in text:
            profile["Любимое"] = text.split("мой любимый", 1)[1].strip()

            user_profile[user_id] = profile
    
        else:

            print("Ошибка Cloudflare:", result)

            answer = "Ошибка связи с AI 🤖"

    except Exception as e:

        print(e)

        answer = "Ошибка связи с AI 🤖"

    user_memory[user_id].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    user_memory[user_id] = user_memory[user_id][-10:]

    await update.message.reply_text(answer)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("normal", normal))

app.add_handler(CommandHandler("fun", fun))

app.add_handler(CommandHandler("lol", lol))

app.add_handler(CommandHandler("cute", cute))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message
    )
)

print("Бот работает")

threading.Thread(target=run_web).start()

app.run_polling()
