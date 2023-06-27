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

async def prontosoccorso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Ecco la lista dei pronto soccorsi nella zona di 
Milano. ⚪️🟢🟡🔴''', reply_markup = InlineKeyboardMarkup(keyboard))

def format_ps_code_message(source):
    return f"""⚪️ {source[0]}\n"""
    f"""🟢 {source[4]}\n"""
    f"""🟡 {source[1]}\n"""
    f"""🔴 {source[2]}\n"""
    f"""Totale {source[3]}"""

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer() 
    nomePS, telefono, apertura, pazientiAttesa, pazientiCarico = await fetch(query.data).values
    attesa, carico = [list(pazientiAttesa.values()), list(pazientiCarico.values())]
    await context.bot.send_message(chat_id=chat_id, text=f"""Il nome del pronto soccorso selezionato è {nomePS}.\n"""
    f"""Il pronto soccorso è attualmente : {apertura}.\n"""
    f"""I pazienti in attesa sono :\n"""
    f"""{format_ps_code_message(attesa)}"""
    f"""I pazienti presi in carico sono :\n"""
    f"""{format_ps_code_message(carico)}""")
    await context.bot.send_contact(chat_id=chat_id,phone_number=telefono, first_name=nomePS)
    #await query.edit_message_text(text="Updated data") Per modificare il messaggio

async def fetch(ospedale):
    response = requests.get(api.API_URL[ospedale])
    data = json.loads(response.text)
    anagraficaPS, statoPS = data[0].values
    nomePS, telefono = anagraficaPS.struttura.denominazione, anagraficaPS.telefono
    apertura = "Aperto" if anagraficaPS.psAperto else "Chiuso"
    pazientiAttesa, pazientiCarico = statoPS.numPazientiInAttesa, statoPS.numPazientiInCarico
    return nomePS, telefono, apertura, pazientiAttesa, pazientiCarico

def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('messaggio', prontosoccorso))
    app.add_handler(MessageHandler(filters.TEXT, button))
    app.add_handler(CallbackQueryHandler(button))
    app.add_error_handler(error)
    print('Ascolto...')
    app.run_polling(poll_interval=1)
