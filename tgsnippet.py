from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

from scryfall import get_image
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['auth']['telegram_token']


def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query,
            title='Search Result',
            input_message_content=InputTextMessageContent(get_image(query))
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


def start(bot, update):

    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    updater.start_polling()


def search(bot, update):
    image = get_image(update.message.text)
    bot.send_message(chat_id=update.message.chat_id, text=image)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

search_handler = MessageHandler(Filters.text, search)
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(inline_caps_handler)

updater.start_polling()
