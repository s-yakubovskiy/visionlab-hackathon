#!/usr/bin/env python

import logging
import requests
import re
import shutil
from random import randrange
from pprint import pprint
from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


WELCOME_MESSAGE = 'Welcome to Machine Can See *_*!\nWe have a nice desktop application to monitor ' \
                  'your activity during PC. You can download it at:\nhttps://github.com/Gleonett/CVnurse/invitations' \
                  '\n\nGood exercices to remove eye\'s strain https://lifehacker.ru/uprazhneniya-dlya-glaz/'

USAGE_MESSAGE = "You can send me a picture to begin with.\n" \
                "Or you can \"/find <insert your query here>\" to get some rand image"
KEYS_bot = "899664750:AAEkC8JPCkoVHQ4f3yRuI4IAUoa-D8W5udI"
KEYS_img = "12775826-547199fe80cd4b41906433e2c"


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class PixGetter:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://pixabay.com/api/?key={}".format(token)
        self.type = "&image_type=photo"

    def get_pix(self, query):
        method = '&q='
        j = self.api_url + method + query + self.type
        logger.info(j)
        resp = requests.get(self.api_url + method + query + self.type)
        try:
            resp.raise_for_status()
        except Exception as exc:
            print(exc)
        else:
            result_json = resp.json()
            x = randrange(0, len(result_json['hits']))
            return result_json['hits'][x]['webformatURL']


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info("Bot Started")
    logger.info("Keys: %s" % KEYS_bot)
    update.message.reply_text(WELCOME_MESSAGE)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('To use me -> send a photo to me (no nudes allowed!) :D')


def find(update, context):
    """Send a message when the command /help is issued."""
    pic = PixGetter(KEYS_img)
    url = pic.get_pix(" ".join(update.message.text.split(' ')[1:]))
    logger.info(url)
    update.message.reply_photo(url)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(WELCOME_MESSAGE)


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    url = 'https://telegram.org/img/t_logo.png'
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def rand_img(update, context):
    """Random art sending"""
    url = get_image_url()
    user = update.message.from_user

    update.message.reply_text("Thinking hard...")
    logger.info("Photo received from %s" % user.first_name)
    photo_id = update.message.photo[-1].file_id
    json_url = ('https://api.telegram.org/bot' + KEYS_bot +
                '/getFile?file_id=' + photo_id)
    logger.info(update.message.photo[-1].file_size)

    logger.info(requests.get(json_url).json())

    file_path = (requests.get(json_url).json())['result']['file_path']
    photo_url = 'https://api.telegram.org/file/bot' + KEYS_bot + "/" + file_path
    logger.info(photo_url)
    dl_file(photo_url, photo_url.split('/')[-1])

    # file = context.getFile(update.message.photo[-1].file_id)
    update.message.reply_photo(url)
    # update.send_photo(chat_id=chat_id, photo=url)


def dl_file(url, out_path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(out_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(KEYS_bot, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("find", find))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, rand_img))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()