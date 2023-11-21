import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils.constant import payload
from utils.utils import CompileResult, lines_output, OutputKind

MESSAGE_LIMIT = 1


def compile(update: Update, context: CallbackContext) -> int:
    user_input = ''.join(context.args)
    if user_input != "":
        text = "Stai compilando questo codice:\n" + user_input
        update.message.reply_html(text)
        result = compiler(update.message.text)
        for msg in result.to_messages(OutputKind.ALL)[:MESSAGE_LIMIT]:
            update.message.reply_html(msg)
    else:
        update.message.reply_html("Non hai inserito nessun codice da compilare")



def compiler(code : str) -> CompileResult:
    payload['code'] = code
    r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
    reply = r.json()
    return CompileResult(
        ok=reply['code'] == 0,
        header=('❌' if reply['code'] != 0 else '✅'),
        asm=lines_output(reply['asm']), output=lines_output(reply['stderr']))

