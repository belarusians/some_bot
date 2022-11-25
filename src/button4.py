from telegram import Update
from telegram.ext import CallbackContext

import user_live_chat

TO_BTN = "button 4"
STATE = "BUTTON_4"


def handler(update: Update, context: CallbackContext) -> str:
    context.user_data['FROM'] = STATE
    user_live_chat.handler(update, context)

    return user_live_chat.STATE


handlers = []
