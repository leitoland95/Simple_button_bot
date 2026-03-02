import os
import threading
import time
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("No se encontró el TOKEN en las variables de entorno.")

# Función que se ejecuta con /start
def start(update, context):
    keyboard = [[InlineKeyboardButton("Presióname", url="https://full-stack-z81t.onrender.com/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Pulsa el botón:", reply_markup=reply_markup)

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

# Servidor mínimo para Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running and alive!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Self-ping para evitar que Render duerma el servicio
def keep_alive():
    url = "https://full-stack-z81t.onrender.com/"
    while True:
        try:
            requests.get(url)
        except Exception as e:
            print("Ping error:", e)
        time.sleep(600)  # cada 10 minutos

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    run_server()