import os
import asyncio
import requests
import time
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = FastAPI()

# -------------------------------
# Logs en memoria
# -------------------------------
logs = []

def log_event(message: str):
    print(message)  # también lo imprime en consola
    logs.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

@app.get("/")
def root():
    log_event("Endpoint raíz consultado")
    return {"status": "ok"}

@app.get("/logs")
def get_logs():
    log_event("Endpoint /logs consultado")
    return {"logs": logs}

# -------------------------------
# Self-ping
# -------------------------------
def keep_alive():
    url = "https://simple-button-bot.onrender.com/"
    log_event("Iniciando self-ping loop")
    while True:
        try:
            requests.get(url)
            log_event("Self-ping exitoso")
        except Exception as e:
            log_event(f"Error en self-ping: {e}")
        time.sleep(600)

# -------------------------------
# Telegram Bot
# -------------------------------
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("Comando /start recibido")
    keyboard = [[InlineKeyboardButton("Abrir página", url="https://full-stack-z81t.onrender.com/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bienvenido, abre la página:", reply_markup=reply_markup)
    log_event("Respuesta enviada con botón")

# -------------------------------
# Integración FastAPI + Bot
# -------------------------------
@app.on_event("startup")
async def startup_event():
    log_event("Evento startup de FastAPI")

    # Self-ping en segundo plano
    asyncio.get_event_loop().run_in_executor(None, keep_alive)
    log_event("Self-ping lanzado en segundo plano")

    # Crear aplicación del bot
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    log_event("Bot inicializado con handler /start")

    # Inicializar y arrancar el bot sin cerrar el loop de FastAPI
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    log_event("Bot arrancado en modo polling")