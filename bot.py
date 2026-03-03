import time
import requests
import os
import asyncio
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# -------------------------------
# FastAPI + self-ping
# -------------------------------
app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}  # Render health check

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

# -------------------------------
# Integración FastAPI + Bot
# -------------------------------
@app.on_event("startup")
async def startup_event():
    # Lanzar self-ping en un hilo aparte
    asyncio.get_event_loop().run_in_executor(None, keep_alive)

    # Crear y lanzar el bot en una tarea asíncrona
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    asyncio.create_task(bot_app.run_polling())