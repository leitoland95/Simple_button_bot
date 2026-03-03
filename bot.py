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
    url = "https://simple-button-bot.onrender.com/"
    while True:
        try:
            requests.get(url)
        except Exception as e:
            print("Error en self-ping:", e)
        time.sleep(600)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Abrir página", url="https://simple-button-bot.onrender.com/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bienvenido, abre la página:", reply_markup=reply_markup)

@app.on_event("startup")
async def startup_event():
    # Self-ping en segundo plano
    asyncio.get_event_loop().run_in_executor(None, keep_alive)

    # Crear aplicación del bot
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))

    # Inicializar y arrancar el bot sin cerrar el loop de FastAPI
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()