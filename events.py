import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

log = logging.getLogger(__name__)
async def ask_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

 """Запрашивает дату у пользователя"""
    message = update.message
    user = update.effective_user
    log.info(f'Функция ask_data вызвана пользователем {user}\n')

    text = [
        f'Привет, {user.first_name}!',
        '',
        'Я - школьный бот, который отправлет Вашу заявку школьным световикам:',
        'Если вы готовы продолжить, напишите дату, когда будет проходить мероприятие.'
    ]
    text = '\n'.join(text)

    await update.message.reply_text(f'{text}')
    pass

async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на запрос дату"""
    pass

async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запрашивает место проведения у пользователя"""

async def say_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает inline-клавиатуру"""
    user = update.effective_user
    log.info(f'Функция say_place вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Актовый зал', callback_data='Актовый зал'),
            InlineKeyboardButton('Двор', callback_data='Двор')],
            InlineKeyboardButton('Другое', callback_data='Другое')
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Где именно вы хотели бы провести мероприятие?',
        reply_markup=keyboard
        )

async def react_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'inline-клавиатура'"""
    user = update.effective_user
    log.info(f'Функция react_place вызвана пользователем {user}')

    query = update.callback_query

    buttons = [
        [InlineKeyboardButton('Актовый зал', callback_data='Актовый зал'),
            InlineKeyboardButton('Двор', callback_data='Двор')],
            InlineKeyboardButton('Другое', callback_data='Другое')
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text='Где именно вы хотели бы провести мероприятие?',
        reply_markup=keyboard
        )

    pass

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на сообщение о место проведения мероприятия"""
    pass

async def ask_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Уточняет сферу работы для световика у пользователя"""
    pass

async def get_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на запрос о сфере работы световика"""
    pass

async def ask_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Уточняет, кого пользователь хотел бы видеть из световиков"""
    pass

async def get_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на запрос определенного световика"""
    pass

async def ask_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Просит проверить пользователя итоговое сообщение"""
    pass

async def get_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на проверку пользователя на итоговое сообщение"""
    pass



app.add_handler(CommandHandler("hello", ask_data()))