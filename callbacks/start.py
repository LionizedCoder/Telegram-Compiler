from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    text = "<b>Ciao <i>{}</i>, benvenuto su Compiler Bot!</b>\n".format(user_name)
    text += "Questo bot ti permette di mandare un codice al bot e controllare l'output!\n"
    text += "Attualmente l'unico linguaggio supportato è <b>Rust</b>!\n"
    update.message.reply_html(
        text, reply_to_message_id=update.message.message_id)