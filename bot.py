import os
import asyncio
import requests
import time
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

def keep_alive():
    url = "https://full-stack-z81t.onrender.com/"
    while True:
        try:
            requests.get(url)
        except Exception as e:
            print("Error en self-ping:", e)
        time.sleep(600)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Abrir página", url="https://full-stack-z81t.onrender.com/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bienvenido, abre la página:", reply_markup=reply_markup)

@app.on_event("startup")
async def startup_event():
    # Self-ping en segundo plano
    asyncio.get_event_loop().run_in_executor(None, keep_alive)

    # Crear aplicación del bot
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))

    # Importante: usar la versión awaitable
    asyncio.create_task(bot_app.run_polling(close_loop=False))