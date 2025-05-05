import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          CallbackQueryHandler,
                          ConversationHandler,
                          filters)

from services import get_worker_list

log = logging.getLogger(__name__)
WAIT_FOR_DATE, WAIT_FOR_PLACE, WAIT_FOR_WORKER, WAIT_FOR_CHECK, WAIT_FOR_EQUIPMENT = range(5)


async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_date is triggered by {update.effective_user}')
    text = 'Когда будет мероприятие?'
    await update.message.reply_text(text)

    return WAIT_FOR_DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'get_date is triggered by {update.effective_user}')
    day = update.message.text
    context.user_data["дата"] = update.message.text
    text = f'Я понял, мероприятие в эту дату: {update.message.text}'
    await update.message.reply_text(text)

    return await ask_place(update, context)


async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'ask_place is triggered by {update.effective_user}')
    buttons = [
        [InlineKeyboardButton('Зал', callback_data='Зал'),
         InlineKeyboardButton('Двор', callback_data='Двор')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Где именно будет проходить мероприятие?',
        reply_markup=keyboard
    )

    return WAIT_FOR_PLACE


async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на сообщение о месте проведения мероприятия"""
    user = update.effective_user
    log.info(f'get_place is triggered by {update.effective_user}')
    query = update.callback_query
    place = update.message.text
    context.user_place['Место проведения']
    await query.answer('Зафиксировали')

    return await register_application(update, context)


async def ask_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показывает inline-клавиатуру, которая спрашиват у пользователя сферу работы для световика"""
    user = update.effective_user
    log.info(f'Функция ask_equipment вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Свет', callback_data='Свет'),
         InlineKeyboardButton('Звук', callback_data='Звук')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='В какой сфере нужна работа световика на мероприятии?',
        reply_markup=keyboard
    )
    return WAIT_FOR_EQUIPMENT


async def get_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на запрос о сфере работы световика"""
    user = update.effective_user
    log.info(f'Функция get_equipment вызвана пользователем {user}')
    query = update.callback_query
    equipment = update.message.text
    context.user_equipment["оборудование"] = update.message.text
    await query.answer('Зафиксировано')
    return await ask_worker(update, context)


async def ask_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Уточняет, кого пользователь хотел бы видеть из световиков"""
    log.info(f'ask_person is triggered by {update.effective_user}')
    workers = get_worker_list()
    buttons = [[InlineKeyboardButton(text='Любой', callback_data='Любой')]
    for person is workers:
        buttons.append([InlineKeyboardButton(text=worker, callback_data=worker)])
    keyboard = InlineKeyboardMarkup(buttons)

    return WAIT_FOR_WORKER



async def get_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на запрос  на определенного световика"""
    user = update.effective_user
    log.info(f'Функция get_person вызвана пользователем {user}')
    return await ask_check(update, context)


async def ask_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Просит проверить пользователя итоговое сообщение"""

    return WAIT_FOR_CHECK


async def get_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на проверку пользователя итогового сообщения"""
    user = update.effective_user
    log.info(f'Функция get_check вызвана пользователем {user}')
    return await ask_check(update, context)


async def register_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f'register_application is triggered by {update.effective_user}')
    day = context.user_data["day"]
    place = update.callback_query.data
    text = 'Заявка зарегистрирована'
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text
    )
    return ConversationHandler.END


events_application_handler = ConversationHandler(
    entry_points=[CommandHandler('events', ask_date)],
    states={
        WAIT_FOR_DATE: [MessageHandler(filters.TEXT, get_date)],
        WAIT_FOR_PLACE: [CallbackQueryHandler(get_place)],
        WAIT_FOR_WORKER: [CallbackQueryHandler(get_worker)],
        WAIT_FOR_CHECK: [MessageHandler(filters.TEXT, get_check)],
        WAIT_FOR_EQUIPMENT: [CallbackQueryHandler(get_equipment)]
    },
    fallbacks=[]
)