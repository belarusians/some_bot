import json
import logging

from telegram import Update
from telegram.ext import CallbackContext


TEST_GROUP = -807787002


logger = logging.getLogger(__name__)


def notify(context: CallbackContext) -> None:
    context_text = json.dumps(context.user_data, ensure_ascii=False)
    notify_with_text(context_text, context)


def notify_with_document(update: Update, context: CallbackContext) -> None:
    if not update.message.document:
        logger.error("Карыстальнік паслаў файл, але нешта пайшло ня так")
        notify_with_text("Карыстальнік паслаў файл, але нешта пайшло ня так, глядзіце логі", context)
    caption = json.dumps(context.user_data, ensure_ascii=False)
    context.bot.send_document(chat_id=TEST_GROUP, document=update.message.document, caption=caption)


def notify_with_text(text: str, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=TEST_GROUP, text=text)
