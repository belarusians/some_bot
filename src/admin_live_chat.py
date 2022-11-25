import json

from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters

STATE = "live_chat"


def handler(update: Update, context: CallbackContext) -> str:
    message_data = update.effective_message.reply_to_message.text or update.effective_message.reply_to_message.caption
    data = json.loads(message_data)

    reply_to_id = data['MESSAGE_ID']
    context.bot.send_message(chat_id=data['CHAT_ID'], text=update.message.text, reply_to_message_id=reply_to_id)
    return STATE


handlers = [
    MessageHandler(Filters.reply, handler),
]
