from telegram import Update
from telegram.ext import CallbackContext

import free_text

TO_BTN = "button 4"
STATE = "BUTTON_4"


def handler(update: Update, context: CallbackContext) -> str:
    context.user_data['FROM'] = STATE
    free_text.handler(update, context)

    return free_text.STATE


handlers = []
