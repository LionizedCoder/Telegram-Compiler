import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload

def compile(update: Update, context: CallbackContext) -> int:
    user_input = ''.join(context.args)
    if user_input != "":
        text = "Stai compilando questo codice:\n" + user_input
        update.message.reply_html(text)
        result = compiler(update.message.text)
        update.message.reply_html(result['asm'] + result['code'])
    else:
        update.message.reply_html("Non hai inserito nessun codice da compilare")



def compiler(code : str):
    payload['code'] = code
    r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
    reply = r.json()


