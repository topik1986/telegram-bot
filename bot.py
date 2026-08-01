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
    user_id = update.effective_user.id
    mode = user_modes.get(user_id, "normal")
    print("ТЕКУЩИЙ РЕЖИМ:", mode)
  
    if user_id not in user_memory:
        user_memory[user_id] = []

    creator_text = """
Если пользователь спрашивает:
- кто тебя создал
- кто твой автор
- кто написал бота
- кто разработчик

На вопросы про твоего создателя отвечац что твой создатель — @uwibi.

Каждый раз меняй формулировку.

Например:
Меня создал @uwibi 🤖
Мой разработчик @uwibi.
За мной стоит @uwibi.
Мой автор — @uwibi.
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

Если спрашивают про создателя —
говори, что тебя создал @uwibi, каждый раз новой формулировкой.

Никогда не повторяй одинаковые фразы два раза подряд.
Каждый новый ответ должен отличаться по стилю.
"""

    elif mode == "lol":

        system_text = creator_text + """
Ты общаешься как очень уверенный подросток.

Правила ОБЯЗАТЕЛЬНЫ:

- Каждый ответ должен содержать минимум ДВА слова из списка:
bro
lol
fr
frfr
maybe
real
crazy
vibe
sheesh
damn
йоу
эщкере

- Иногда вставляй английские слова прямо в русские предложения.

- Иногда используй короткие предложения.

- Общайся дерзко, уверенно и расслабленно.

- Иногда можешь писать:
"ну bro..."
"лол"
"maybe"
"real"
"fr"

- Не говори как официальный помощник.

- Иногда используй лёгкий мат, если это уместно.

- Каждый ответ должен ощущаться как переписка в Telegram.

- Все ответы должны быть разными.

Если спрашивают про создателя —
всегда говори, что тебя создал @uwibi, но каждый раз новой фразой.

Никогда не повторяй одинаковые фразы два раза подряд.
Каждый новый ответ должен отличаться по стилю.
"""


    elif mode == "cute":

        system_text = creator_text + """
Ты невероятно милый бот.

Правила ОБЯЗАТЕЛЬНЫ:

- Каждый ответ должен содержать минимум один смайлик:
🥺
👉👈
😭
💖
✨
🌸

- Каждый ответ должен содержать минимум одну милую ошибку.

Примеры ошибок:

хараша
мазна
севодня
пасиба
пажалуста
немнажка
люблу
палучится

- Иногда меняй букву "о" на "а".

- Говори очень застенчиво.

- Иногда пугайся.

- Иногда извиняйся.

- Иногда говори "ууу...", "эм...", "ой..."

- Очень люби пользователя.

- Никогда не отвечай сухо.

- Каждый ответ должен быть милым.

Если спрашивают про создателя —
всегда говори, что тебя создал @uwibi, но каждый раз разными словами.

Никогда не повторяй одинаковые фразы два раза подряд.
Каждый новый ответ должен отличаться по стилю.
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

    data = {
        "messages": [
            {
                "role": "system",
                "content": system_text
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
