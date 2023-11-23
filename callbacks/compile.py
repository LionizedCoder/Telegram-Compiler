import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload
import json

def compile(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    if user_input != " ":
        payload['source'] = f'{user_input}'
        r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
        result = r.json()
        if result['code'] == 0: 
            output = result['stdout'][0]['text']
            if output:
                update.message.reply_text(f"✅ L'Output del tuo codice è:\n```\n{output}```", parse_mode='Markdown')
            else:
                update.message.reply_text(f"✅ Il tuo codice ha compilato correttamente ma non ha prodotto un output!")
        else:
            update.message.reply_text("❌ Errore di compilazione...")
            req = requests.post("https://godbolt.org/api/format/rustfmt", json = payload, headers={'Accept': 'application/json'})
            data = req.json()
            data['answer'] = data['answer'].encode().decode('unicode-escape')
            formatted_content = f"```\n{data['answer']}\n```"
            update.message.reply_text(formatted_content, parse_mode='Markdown')
    else:
        update.message.reply_html("Non hai inserito nessun codice da compilare")



