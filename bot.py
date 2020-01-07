import logging
from glob import glob
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler


import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(bot, update, user_data):
    emoji = get_user_emoji(user_data)
    text = f'Привет {emoji}'
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать локацию', request_location=True)
    keyboard = ReplyKeyboardMarkup([['/picture', 'Прислать картинку'],
                                    [contact_button, location_button]
                                    ])
    update.message.reply_text(text, reply_markup=keyboard)


def talk_to_me(bot, update, user_data):
    user_text = '{} {}! Ты написал: {}'.format(update.message.chat.first_name, user_data['emoji'], update.message.text)
    logging.info('User: %s, Chat_id: %s, Message: %s', update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)

def send_random_picture(bot, update, user_data):
    picture_list = glob('images/*.*')
    picture = choice(picture_list)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(picture, 'rb'))

def get_contact(bot, update, user_data):
    update.message.reply_text('Спасибо {}!'.format(user_data['emoji']), reply_markup=ReplyKeyboardRemove())
    logging.info(update.message.contact)

def get_location(bot, update, user_data):
    update.message.reply_text('Спасибо {}!'.format(user_data['emoji']))
    logging.info(update.message.location)

def get_user_emoji(user_data):
    if 'emoji' in user_data:
        return user_data['emoji']
    else:
        user_data['emoji'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emoji']

def main():
    mybot = Updater(settings.API_KEY)

    logging.info('Bot running...')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('picture', send_random_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^Прислать картинку$', send_random_picture, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

main()