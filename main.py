from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity, ParseMode, Update
from telegram.ext import CommandHandler, Updater, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging
from utils.constant import token
from callbacks.start import start
from callbacks.decode import decode
from callbacks.compile import compile
from callbacks.formatter import formatted

#Set Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Bot starting...")
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('compile', compile)],
    #     states={WAITING_FOR_REPLY: [MessageHandler(Filters.text & ~Filters.command, fetch_reply)]},
    #     fallbacks=[]
    # )
    # dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler(
        'compile', compile, filters=Filters.text))
    dispatcher.add_handler(CommandHandler(
        'start', start, filters=Filters.text))
    dispatcher.add_handler(CommandHandler(
        'decode', decode, filters=Filters.text))
    dispatcher.add_handler(CommandHandler(
        'format', formatted, filters=Filters.text))
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", webhook_url=f'https://compiler-bot-test.onrender.com/' + token, url_path=token, port=int(5000))
    updater.idle()


