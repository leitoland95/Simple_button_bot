import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("No se encontró el TOKEN en las variables de entorno.")

# Función que se ejecuta con /start
def start(update, context):
    keyboard = [[InlineKeyboardButton("Presióname", callback_data="hola")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Pulsa el botón:", reply_markup=reply_markup)

# Función que se ejecuta cuando se pulsa el botón
def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == "hola":
        query.edit_message_text(text="Hola mundo")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

# Servidor mínimo para Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Arranca el bot en un hilo separado
    threading.Thread(target=run_bot).start()
    # Arranca el servidor mínimo para Render
    run_server()