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
    ChatMemberHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import user_live_chat
import admin_live_chat
import notify
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


def chat_handler(update: Update, context: CallbackContext) -> str:
    if update.my_chat_member.new_chat_member.user.id == context.bot.id:
        if update.my_chat_member.new_chat_member.status == 'member':
            logger.info(f"Bot was added to group {update.effective_chat.id}")
            current_chat_id = update.effective_chat.id
            text = f'{notify.ADMIN_GROUP_NAME}: {current_chat_id}\nПеразапусьціце мяне з гэтым параметрам, каб я змог сюды пісаць'
            context.bot.send_message(chat_id=current_chat_id, text=text)
        else:
            logger.info(f"Bot was removed from group {update.effective_chat.id}")


def main(token) -> None:
    updater = Updater(token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(Filters.reply, admin_live_chat.handler),
            ChatMemberHandler(callback=chat_handler),
            MessageHandler(Filters.all, handle_free_message),
        ],
        states={
            START: start_handlers,
            button1.STATE: [CommandHandler('start', start)],
            button2.STATE: [CommandHandler('start', start)],
            button3.STATE: [CommandHandler('start', start)],
            button4.STATE: [CommandHandler('start', start)],
            user_live_chat.STATE: user_live_chat.handlers + [CommandHandler('start', start)],
            admin_live_chat.STATE: admin_live_chat.handlers,
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
