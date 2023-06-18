from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes , CallbackQueryHandler


print('Mi sto avviando')

TOKEN: Final = ''
BOT_USERNAME: Final = ''
keyboard = [
        [InlineKeyboardButton("San Raffaele", callback_data='SanRaffaele')],
        [InlineKeyboardButton("Ospedale di Melzo", callback_data='Melzo')],
    ]
reply_markup = InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Ciao 👋🏻 mi presento sono ProntoSoccorso Bot, con me potrai controllare in tempo reale
lo stato dei pronto soccorso nella provincia di Milano. ⚪️🟢🟡🔴''', reply_markup = InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()

    if query.data == 'Melzo':
        query.edit_message_text(text="Ciao!")
    elif query.data =="SanRaffele":
        query.edit_message_text(text="Ciao!")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(MessageHandler(filters.TEXT, button))
    app.add_handler(CallbackQueryHandler(button))


    app.add_error_handler(error)

    print('Ascolto...')
    app.run_polling(poll_interval=5)
