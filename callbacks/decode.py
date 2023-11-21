from telegram import Update
from telegram.ext import CallbackContext
import requests
import re

def decode(update: Update, context: CallbackContext) -> None:
    user_input = ' '.join(context.args)
    
    url_pattern = re.compile(r'https?://\S+')
    if re.search(url_pattern, user_input):
        match = re.search(r'/z/(\S+)', user_input)
        if match:
            godbolt_id = match.group(1)
            r = requests.get(f'https://godbolt.org/z/{godbolt_id}/code/1')
            content =  r.content.decode('utf-8')
            formatted_content = "```rust\n" + content.replace('\n', '  \n') + "```"
            update.message.reply_text(formatted_content, parse_mode='Markdown')

        else:
            update.message.reply_text("Non hai inserito un link valido di godbolt")
    else:
        update.message.reply_text("Non hai inserito un link.")
    