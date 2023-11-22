import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload

def wall(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    if user_input != " ":
        r = requests.post("https://godbolt.org/api/compiler/r1730/compile", params = {"options": "--emit asm"} , data=user_input ,
        headers = {"Content-Type": "text/plain"})
        if r.status_code == 200:
            assembly = r.text
            update.message.reply_text(assembly)
        else:
            update.message.reply_text("La richiesta non è andata a buon fine, riprova.")
    else:
        update.message.reply_html("Non hai inserito nessun codice")