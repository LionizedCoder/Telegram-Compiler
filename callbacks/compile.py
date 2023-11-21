import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload

def compile(update: Update, context: CallbackContext) -> int:
    user_input = ''.join(context.args)
    if user_input != "":
        text = "Stai compilando questo codice:\n" + f"```rust\n{user_input}```"
        update.message.reply_text(text, parse_mode='Markdown')
        payload['code'] = user_input
        r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
        update.message.reply_html("<b>In costruzione..</b>")
        # result = r.text
        # update.message.reply_html(result)
    else:
        update.message.reply_html("Non hai inserito nessun codice da compilare")



