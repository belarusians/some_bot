from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, MessageHandler, Filters, ConversationHandler

import notify

READY_BTN = "Скончыць дыялог"
MSG = "Вы ўвайшлі ў чат з намі. Каб выйсьці з чату націсніце \"{}\"".format(READY_BTN)
STATE = "user_live_chat"


def handler(update: Update, context: CallbackContext) -> str:
    context.user_data["CHAT_ID"] = update.message.chat_id
    context.user_data["MESSAGE"] = ''
    reply_keyboard = [[READY_BTN]]
    update.message.reply_text(
        MSG,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return STATE


def finish_conversation_handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Дзякуй! Вы можаце пачаць працэс зноў націснуўшы /start",
        reply_markup=ReplyKeyboardRemove(),
    )

    notify.notify_with_text("Карыстальнік скончыў дыялог. Ён не зможа болей вам адказваць, таму пісаць яму, пакуль ён не пачне дыялог зноў, - бессэнсоўна", context)

    return ConversationHandler.END


def free_text_handler(update: Update, context: CallbackContext) -> str:
    if 'MESSAGE' in context.user_data:
        context.user_data["MESSAGE"] += "\n {}".format(update.message.text)
    else:
        context.user_data["MESSAGE"] = update.message.text

    context.user_data['MESSAGE_ID'] = update.message.message_id

    notify.notify(context)

    return STATE


def handle_file(update: Update, context: CallbackContext) -> str:
    context.user_data['MESSAGE_ID'] = update.message.message_id

    notify.notify_with_document(update, context)

    return STATE


handlers = [
    MessageHandler(Filters.regex(READY_BTN), finish_conversation_handler),
    MessageHandler(Filters.document, handle_file),
    MessageHandler(Filters.text, free_text_handler),
]
