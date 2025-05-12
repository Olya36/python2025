import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          CallbackQueryHandler,
                          filters,
                          ConversationHandler)

from services import get_worker_list

log = logging.getLogger(__name__)
(WAIT_FOR_DATE,
 WAIT_FOR_PLACE,
 WAIT_FOR_EQUIPMENT,
 WAIT_FOR_WORKER) = range(4)


async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрашивает дату у пользователя"""
    user = update.effective_user
    message = update.message
    log.info(f'Функция ask_date вызвана пользователем {user}\n')
    text = [

        f'Здрвствуйте, {user.first_name}',
        'Я - школьный бот, который отправляет Вашу заявку школьным световикам.',
        'Если Вы готовы продолжить, напишите дату, когда будет проходить мероприятие.'
        'Пожалуйста, пишите дату в формате ДД.ММ.ГГГГ'
    ]
    text = '\n'.join(text)

    await update.message.reply_text(f'{text}')
    return WAIT_FOR_DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на запрос даты"""
    user = update.effective_user
    log.info(f'Функция ask_date вызвана пользователем {user}\n')
    day = update.message.text
    context.user_data["дата"] = update.message.text
    text = f'Я понял, мероприятие в эту дату: {update.message.text}'
    return await ask_place(update, context)


async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показывает inline-клавиатуру, которая спрашиват у пользователя место проведения мероприятия"""
    user = update.effective_user
    log.info(f'Функция ask_place вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Акт. зал', callback_data='Акт. зал'),
         InlineKeyboardButton('Двор', callback_data='Двор')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Где именно Вы хотели бы провести мероприятие?',
        reply_markup=keyboard
    )
    return WAIT_FOR_PLACE



async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на сообщение о месте проведения мероприятия"""
    user = update.effective_user
    query = update.callback_query
    log.info(f'Функция get_place вызвана пользователем {user}')
    place = query.data
    context.user_data['Место'] = place
    text = f'Я порнял, мероприятие в этом месте: {query.data}'
    await query.answer('Зафиксировано')
    return await ask_equipment(update, context)


async def ask_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показывает inline-клавиатуру, которая спрашиват у пользователя сферу работы для световика"""
    user = update.effective_user
    log.info(f'Функция ask_equipment вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Свет', callback_data='Свет'),
         InlineKeyboardButton('Звук', callback_data='Звук')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    query = update.callback_query
    await query.edit_message_text(
        text='В какой сфере нужна работа световика на мероприятии?',
        reply_markup=keyboard
    )
    return WAIT_FOR_EQUIPMENT


async def get_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на запрос о сфере работы световика"""
    user = update.effective_user
    log.info(f'Функция get_equipment вызвана пользователем {user}')
    query = update.callback_query
    await query.answer('Зафиксировано')
    return await ask_worker(update, context)


async def ask_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Уточняет, кого пользователь хотел бы видеть из световиков"""
    user = update.effective_user
    log.info(f'Функция ask_worker вызвана пользователем {user}')
    workers = get_worker_list()
    buttons = [[InlineKeyboardButton(text='Любого', callback_data='Любого')]]
    for worker in workers:
        buttons.append([InlineKeyboardButton(text=worker, callback_data=worker)])
    keyboard = InlineKeyboardMarkup(buttons)
    # Сделать клавиатуру по ФИО световиков | по классам
    query = update.callback_query

    await query.edit_message_text(
        text='Кого бы Вы хотели видеть?',
        reply_markup=keyboard
    )

    return WAIT_FOR_WORKER


async def get_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Реагирует на запрос на определённого световика"""
    user = update.effective_user
    log.info(f'Функция get_worker вызвана пользователем {user}')
    query = update.callback_query
    await query.answer('Зафиксировано')

    return await registr_application(update, context)




#async def get_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#    """Реагирует на проверку пользователем итогового сообщения"""
#    user = update.effective_user
#    log.info(f'Функция get_check вызвана пользователем {user}')

#    return await registr_application(update, context)

async def registr_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Окончательное сообщение"""
    log.info(f'register_application is triggered by {update.effective_user}')
    day = context.user_data["дата"]
    place = context.user_place["Место"]
    worker = update.callback_query
    text = ('Заявка зарегистрирована:\n'
            f'Дата: {day}\n'
            f'Работник: {worker}\n'
            f'Место: {place}\n'
            )
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
        WAIT_FOR_EQUIPMENT: [CallbackQueryHandler(get_equipment)],
        WAIT_FOR_WORKER: [CallbackQueryHandler(get_worker)]
    },
    fallbacks=[]
)
