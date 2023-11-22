import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import formatted_payload, headers
import json
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

def formatted(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    if user_input != " ":
        formatted_payload['source'] = f'{user_input}'
        logger.debug(formatted_payload['source'])
        logger.debug(formatted_payload)
        r = requests.post("https://godbolt.org/api/format/rustfmt", json = formatted_payload, headers= headers)
        try:
            data = r.json()
        except Exception as e:
            logger.error(e)
        data['answer'] = data['answer'].encode().decode('unicode-escape')
        formatted_content = f"```rust\n{data['answer']}\n```"
        update.message.reply_text(formatted_content, parse_mode='Markdown')
    else:
        update.message.reply_html("Non hai inserito nessun codice da formattare")