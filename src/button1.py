from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

TO_BTN = 'button 1'
STATE = 'BUTTON_1'
MSG = "Informational message 1"


def handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(MSG)

    return ConversationHandler.END


handlers = []
