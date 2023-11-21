import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload
from utils.utils import CompileResult, lines_output


WAITING_FOR_REPLY = 1

def compile(update: Update, context: CallbackContext) -> int:
    user_name = update.message.from_user.first_name
    text = "Siamo felici che tu voglia usare questo bot!\n".format(user_name)
    text += "Come prossimo messaggio invia il codice da compilare in <b>Rust</b>"
    update.message.reply_html(
        text, reply_to_message_id=update.message.message_id)
    return  WAITING_FOR_REPLY

def fetch_reply(update: Update, context: CallbackContext):
    text = "Stai compilando questo codice:\n"
    update.message.reply_html(text)
    result = compiler(update.message.text)


def compiler(code : str) -> str:
    payload['code'] = code
    r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
    reply = r.json()
    return CompileResult(
        ok=reply['code'] == 0,
        header=('❌' if reply['code'] != 0 else '✅'),
        asm=lines_output(reply['asm']), output=lines_output(reply['stderr']))

