import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

def compile(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    if user_input != " ":
        payload['source'] = f'{user_input}'
        logger.debug(payload)
        r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
        result = r.json()
        
        if result['code'] == 0: 
            output = result['stdout'][0]['text']
            update.message.reply_text(f"✅ L'Output del tuo codice è:\n```{output}```", parse_mode='Markdown')
        else:
            update.message.reply_text("❌ Errore di compilazione... La gestione dell'errore verrà implementata a breve")
    else:
        update.message.reply_html("Non hai inserito nessun codice da compilare")



