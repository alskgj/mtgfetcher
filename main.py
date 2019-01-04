import configparser

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import Updater

from scryfall import get_all

import logging
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['auth']['telegram_token']


def inline_article(bot, update):
    query = update.inline_query.query
    if not query or len(query) < 3:
        return
    data = get_all(query)
    results = list()
    for card in data:
        results.append(
            InlineQueryResultArticle(
                id=card['id'],
                title=card['name'],
                input_message_content=InputTextMessageContent(card['png']),
            )
        )
    bot.answer_inline_query(update.inline_query.id, results)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

inline_article_handler = InlineQueryHandler(inline_article)
dispatcher.add_handler(inline_article_handler)

updater.start_polling()
