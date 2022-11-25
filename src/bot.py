#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from typing import Callable

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import free_text
import operator2
import button1
import button2
import button3
import button4

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

START = "start"
GREETINGS_MSG = "Вітаем! Тыкайце!"


def start(update: Update, context: CallbackContext) -> str:
    # context.user_data.clear()
    reply_keyboard = [[button1.TO_BTN, button2.TO_BTN, button3.TO_BTN, button4.TO_BTN]]

    update.message.reply_text(
        GREETINGS_MSG,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return START


def restarter(hndlr: Callable[[Update, CallbackContext], str]) -> Callable[[Update, CallbackContext], str]:
    def inner(update: Update, context: CallbackContext):
        hndlr(update, context)

        return start(update, context)

    return inner


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("User canceled the conversation")
    update.message.reply_text('Дзякуй, да пабачэння', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


start_handlers = [
    MessageHandler(Filters.regex(button1.TO_BTN), restarter(button1.handler)),
    MessageHandler(Filters.regex(button2.TO_BTN), button2.handler),
    MessageHandler(Filters.regex(button3.TO_BTN), restarter(button3.handler)),
    MessageHandler(Filters.regex(button4.TO_BTN), button4.handler),
]


def handle_free_message(update: Update, context: CallbackContext) -> str:
    # if 'CHAT_ID' not in context.user_data or 'STATE' not in context.user_data:
    #     return restarter(start)(update, context)

    # if context.user_data['STATE'] == button2.STATE:
    #     return button2.free_text_handler(update, context)
    # elif context.user_data['STATE'] == button4.STATE:
    #     return button4.free_text_handler(update, context)

    if update.message.chat.type != 'group':
        return start(update, context)


def main(token) -> None:
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.reply, operator2.handler),
            MessageHandler(Filters.all, handle_free_message)
        ],
        states={
            START: start_handlers,
            button1.STATE: button1.handlers + [CommandHandler('start', start)],
            button2.STATE: button2.handlers + [CommandHandler('start', start)],
            button3.STATE: button3.handlers + [CommandHandler('start', start)],
            button4.STATE: button4.handlers + [CommandHandler('start', start)],
            free_text.STATE: free_text.handlers + [CommandHandler('start', start)],
            operator2.STATE: operator2.handlers,
        },
        fallbacks=[
            CommandHandler('cancel', cancel)
        ],
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    TOKEN = sys.argv[1]
    main(TOKEN)