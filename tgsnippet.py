import configparser

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultPhoto
from telegram.ext import Updater

from scryfall import get_all

import logging
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['auth']['telegram_token']


def inline_article(bot, update):
    query = update.inline_query.query
    if not query:
        return
    data = get_all(query)
    results = list()
    for card in data:
        results.append(
            InlineQueryResultArticle(
                id=card['name'],
                title=card['name'],
                input_message_content=InputTextMessageContent(card['png']),
            )
        )
    bot.answer_inline_query(update.inline_query.id, results)


def inline_photo(bot, update):
    query = update.inline_query.query
    if not query:
        return
    data = get_all(query)
    results = list()
    for card in data:
        results.append(
            InlineQueryResultPhoto(
                id=card['name'],
                photo_url=card['png'],
                thumb_url=card['thumbnail']
            )
        )
    print(f'query: {query} answerlength: {len(results)}')
    bot.answer_inline_query(update.inline_query.id, results)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# inline_photo_handler = InlineQueryHandler(inline_photo)
# dispatcher.add_handler(inline_photo_handler)

inline_article_handler = InlineQueryHandler(inline_article)
dispatcher.add_handler(inline_article_handler)

updater.start_polling()
