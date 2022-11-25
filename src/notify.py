import json
import logging
import os

from telegram import Update
from telegram.ext import CallbackContext


ADMIN_GROUP_NAME = 'ADMIN_GROUP'
ADMIN_GROUP = os.environ.get(ADMIN_GROUP_NAME)

logger = logging.getLogger(__name__)


def notify(context: CallbackContext) -> None:
    context_text = json.dumps(context.user_data, ensure_ascii=False)
    notify_with_text(context_text, context)


def notify_with_document(update: Update, context: CallbackContext) -> None:
    if not os.environ.get(ADMIN_GROUP_NAME):
        logger.warning(f'{ADMIN_GROUP_NAME} env variable has to be set, otherwise bot will not support live chat')
    if not update.message.document:
        logger.error(f'User has sent the file, but something went wrong')
        notify_with_text("Карыстальнік паслаў файл, але нешта пайшло ня так, глядзіце логі", context)
    caption = json.dumps(context.user_data, ensure_ascii=False)
    context.bot.send_document(chat_id=ADMIN_GROUP, document=update.message.document, caption=caption)


def notify_with_text(text: str, context: CallbackContext) -> None:
    if not os.environ.get(ADMIN_GROUP_NAME):
        logger.warning(f'{ADMIN_GROUP_NAME} env variable has to be set, otherwise bot will not support live chat')
    context.bot.send_message(chat_id=ADMIN_GROUP, text=text)
