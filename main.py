from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Updater
import requests
import const as api
import json
import os

print('Mi sto avviando')

TOKEN = os.environ['BOT_TOKEN']
BOT_USERNAME = '@prontosoccorsostatobot'
HOSTING_URL = os.environ["H_URL"]
keyboard = [
    [InlineKeyboardButton("🏥 San Raffaele", callback_data='SanRaffaele')],
    [InlineKeyboardButton("🏥 Ospedale San Carlo Borromeo", callback_data='SanCarloBorromeo')],
    [InlineKeyboardButton("🏥 Ospedale di Melzo", callback_data='OspedaleMelzo')],
]
reply_markup = InlineKeyboardMarkup(keyboard)

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text('''Ciao 👋🏻 mi presento sono ProntoSoccorso Bot, con me potrai controllare in tempo reale
    lo stato dei pronto soccorso nella provincia di Milano. ⚪️🟢🟡🔴''', reply_markup=reply_markup)

def prontosoccorso(update: Update, context: CallbackContext):
    update.message.reply_text('''Ecco la lista dei pronto soccorsi nella zona di 
    Milano. ⚪️🟢🟡🔴''', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    contenuto = fetch(query.data)
    attesa = list(contenuto[3].values())  # bianchi, gialli, rossi, totale, verde
    carico = list(contenuto[4].values())  # bianchi, gialli, rossi, totale, verde
    query.message.reply_text(f"""Il nome del pronto soccorso selezionato è """
                             f"""{contenuto[0]}.\nIl pronto soccorso è attualmento : {contenuto[2]}.\nI """
                             f"""pazienti in attesa sono :\n⚪️ {attesa[0]}\n🟢 {attesa[4]}\n🟡 {attesa[1]}\n🔴 {attesa[2]}\nTotale {attesa[3]}"""
                             f"""\nI pazienti presi in carico sono :\n⚪️ {carico[0]}\n🟢 {carico[4]}\n🟡 {carico[1]}\n🔴 {carico[2]}\nTotale {carico[3]}""")
    query.message.reply_contact(phone_number=contenuto[1], first_name=contenuto[0])
    # query.edit_message_text(text="Updated data") Per modificare il messaggio

def fetch(ospedale):
    response = requests.get(api.API_URL[ospedale])
    data = json.loads(response.text)
    nomePS = data[0]["anagraficaPS"]["struttura"]["denominazione"]
    telefono = data[0]["anagraficaPS"]["telefono"]
    apertura = data[0]["anagraficaPS"]["psAperto"]
    if apertura == True:
        apertura = "Aperto"
    else:
        apertura = "Chiuso"
    pazientiAttesa = data[0]["statoPS"]["numPazientiInAttesa"]
    pazientiCarico = data[0]["statoPS"]["numPazientiInCarico"]
    return nomePS, telefono, apertura, pazientiAttesa, pazientiCarico

def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('messaggio', prontosoccorso))
    dispatcher.add_handler(MessageHandler(Filters.text, button))

    dispatcher.add_error_handler(error)

    print('Ascolto...')
    updater.start_polling()
