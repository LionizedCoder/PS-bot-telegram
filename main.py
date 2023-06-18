from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes , CallbackQueryHandler
import requests
import const as api
import json
print('Mi sto avviando')

TOKEN: Final = ''
BOT_USERNAME: Final = ''
keyboard = [
        [InlineKeyboardButton("🏥 San Raffaele", callback_data='SanRaffaele')],
        [InlineKeyboardButton("🏥 Ospedale San Carlo Borromeo", callback_data='SanCarloBorromeo')],
        [InlineKeyboardButton("🏥 Ospedale di Melzo", callback_data='OspedaleMelzo')],

    ]
reply_markup = InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Ciao 👋🏻 mi presento sono ProntoSoccorso Bot, con me potrai controllare in tempo reale
lo stato dei pronto soccorso nella provincia di Milano. ⚪️🟢🟡🔴''', reply_markup = InlineKeyboardMarkup(keyboard))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 
    contenuto = await fetch(query.data)
    await context.bot.send_message(chat_id=query.message.chat_id, text=(contenuto))
    #await query.edit_message_text(text="Updated data") Per modificare il messaggio

async def fetch(ospedale):
    response = requests.get(api.API_URL[ospedale])
    data = json.loads(response.text)
    print(data['anagraficaPS'])
    return

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def updateApi():
    print("texjsi")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT, button))
    app.add_handler(CallbackQueryHandler(button))
    app.add_error_handler(error)
    print('Ascolto...')
    app.run_polling(poll_interval=1)
