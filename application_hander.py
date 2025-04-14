import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          CallbackQueryHandler,
                          filters,
                          ConversationHandler)


log = logging.getLogger(__name__)
WAIT_FOR_DATA, WAIT_FOR_PLACE = range(2)

async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_date is triggered by {update.effective_user}')
    text = 'Когда будет мероприятие?'
    await update.message.reply_text(text)
    return WAIT_FOR_DATA
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_date is triggered by {update.effective_user}')
    text = 'Я понял, мероприятие в эту дату: {update.message.text'
    await update.message.reply_text(text)
    return await ask_place(update, context)

async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_place is triggered by {update.effective_user}')
    query = update.callback_query

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass


events_application_handler = ConversationHandler(
    entry_points=[CommandHandler('events', ask_date())],
    states={
        WAIT_FOR_DATA: [],
        WAIT_FOR_PLACE: [],
    },
    fallbacks=[]
)