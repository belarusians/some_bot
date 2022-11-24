from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

TO_BTN = 'button 3'
STATE = 'BUTTON_3'
MSG = "Informational message 3"


def handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(MSG)

    return ConversationHandler.END


handlers = []
