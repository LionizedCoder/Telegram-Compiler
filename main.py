from io import BytesIO
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity, ParseMode, Update
from telegram.ext import CommandHandler, Updater, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging
import re
from enum import Flag, auto
import os
from dataclasses import dataclass


class OutputKind(Flag):
    ASM = auto()
    OUTPUT = auto()
    ALL = ASM | OUTPUT

@dataclass
class CompileResult:
    ok: bool
    header: str
    asm: list[str]
    output: list[str]


def lines_output(output):
    return [escape_ansi(line['text']) for line in output]


def escape_ansi(text):
    """Remove ANSI escape codes"""
    text = re.sub(r'\x1b\[([\d;]*?)m', '', text)
    text = text.replace('\x1b[K', '')
    return text


#Set Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

WAITING_FOR_REPLY = 1

def compile(update: Update, context: CallbackContext) -> int:
    user_name = update.message.from_user.first_name
    text = "Siamo felici che tu voglia usare questo bot!\n".format(user_name)
    text += "Come prossimo messaggio invia il codice da compilare in <b>Rust</b>"
    logger.info(text)
    update.message.reply_html(
        text, reply_to_message_id=update.message.message_id)
    return  WAITING_FOR_REPLY

def fetch_reply(update: Update, context: CallbackContext):
    text = "Stai compilando questo codice:\n"
    update.message.reply_html(text)
    result = compiler(update.message.text)
    logging.info(result)


def compiler(code : str) -> str:
    payload = {
        "source": code,
          "compiler": "r1730",
        "options": {
            "userArguments": "",
            "compilerOptions": {},
            "filters": {
                "intel": False,
            },
            "tools": [],
            "libraries": [
                {"id": "boost", "version": "181"},
                {"id": "fmt", "version": "trunk"},
                {"id": "rangesv3", "version": "trunk"}
            ]
        },
        "lang": "rust",
        "bypassCache": False,
        "allowStoreCodeDebug": True
    }
    r = requests.post(f"https://godbolt.org/api/compiler/r1730/compile",  json=payload,
        headers={'Accept': 'application/json'})
    reply = r.json()
    return CompileResult(
        ok=reply['code'] == 0,
        header=('❌' if reply['code'] != 0 else '✅'),
        asm=lines_output(reply['asm']), output=lines_output(reply['stderr']))
    


    # update.message.reply_photo(
    #         generate_image(update.message.text))

# def generate_image(code: str):
#     logger.info(f"Creando l'immagine : \n{code}")
#     r = requests.post('https://carbonara.solopov.dev/api/cook',
#                       json={'code': code, 'theme': 'one-dark', 'language': 'text/x-c++src',
#                             'paddingVertical': '10px', 'paddingHorizontal': '10px'})
#     r.raise_for_status()
#     return BytesIO(r.content)
    
def welcome(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name
    text = "<b>Ciao <i>{}</i>, benvenuto su Compiler Bot!</b>\n".format(user_name)
    text += "Questo bot ti permette di mandare un codice al bot e controllare l'output!\n"
    text += "Attualmente l'unico linguaggio supportato è <b>Rust</b>!\n"
    logger.info(text)
    update.message.reply_html(
        text, reply_to_message_id=update.message.message_id)

def main() -> None:
    logger.info("Bot starting...")
    updater = Updater(token=os.environ['TOKEN'], use_context=True)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('compile', compile)],
        states={WAITING_FOR_REPLY: [MessageHandler(Filters.text & ~Filters.command, fetch_reply)]},
        fallbacks=[]
    )
    dispatcher.add_handler(CommandHandler(
        'start', welcome, filters=Filters.text))
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


