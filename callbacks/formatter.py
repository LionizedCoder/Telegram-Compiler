import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import formatted_payload
import json


def formatted(update: Update, context: CallbackContext) -> None:
    user_input = ''.join(context.args)
    formatted_payload['source'] = user_input
    payload = json.dumps(formatted_payload)
    r = requests.post("https://godbolt.org/api/format/rustfmt", json = payload)
    data = r.json()
    data['answer'] = data['answer'].encode().decode('unicode-escape')
    formatted_content = f"```rust\n{data['answer']}\n```"
    update.message.reply_text(formatted_content, parse_mode='Markdown')