import threading
import time
import requests
import os
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# -------------------------------
# FastAPI + self-ping
# -------------------------------
app = FastAPI()

def keep_alive():
    url = "https://full-stack-z81t.onrender.com/"  # tu URL pública en Render
    if not url:
        return
    while True:
        try:
            requests.get(url)
        except Exception as e:
            print("Error en self-ping:", e)
        time.sleep(600)  # cada 10 minutos

@app.on_event("startup")
async def startup_event():
    threading.Thread(target=keep_alive, daemon=True).start()

# -------------------------------
# Telegram Bot
# -------------------------------
TOKEN = os.getenv("TOKEN")  # pon tu token en variable de entorno

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Abrir página", url="https://full-stack-z81t.onrender.com/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bienvenido, abre la página:", reply_markup=reply_markup)

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

# -------------------------------
# Lanzar bot en hilo aparte
# -------------------------------
threading.Thread(target=run_bot, daemon=True).start()