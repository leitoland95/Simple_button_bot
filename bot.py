import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("No se encontró el TOKEN en las variables de entorno.")

# Función que se ejecuta con /start
def start(update, context):
    # Creamos un botón
    keyboard = [[InlineKeyboardButton("Presióname", callback_data="hola")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Enviamos el mensaje con el botón
    update.message.reply_text("Pulsa el botón:", reply_markup=reply_markup)

# Función que se ejecuta cuando se pulsa el botón
def button(update, context):
    query = update.callback_query
    query.answer()  # confirma la acción
    if query.data == "hola":
        query.edit_message_text(text="Hola mundo")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Comando /start
    dp.add_handler(CommandHandler("start", start))

    # Manejo de botones
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()