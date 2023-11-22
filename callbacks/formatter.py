import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import formatted_payload, headers
import json

def formatted(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    if user_input != "":
        formatted_payload['source'] = f'{user_input}'
        r = requests.post("https://godbolt.org/api/format/rustfmt", json = formatted_payload, headers= headers)
        try:
            data = r.json()
            data['answer'] = data['answer'].encode().decode('unicode-escape')
            formatted_content = f"```rust\n{data['answer']}\n```"
            update.message.reply_text(formatted_content, parse_mode='Markdown')
        except Exception as e:
            update.message.reply_text("C'è stato un errore con la tua richiesta, riprova più tardi.")
    else:
        update.message.reply_html("Non hai inserito nessun codice da formattare")