import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

from config import TOKEN
from application_hander import events_application_handler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-10s | %(module)-15s [%(lineno)4d] - %(message)s'
)
logging.getLogger('httpx').setLevel(logging.WARNING)
log = logging.getLogger(__name__)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """функция, которая будет реагировать на команду /hello"""
    user = update.effective_user
    log.info(f'Функция hello вызвана пользователем {user}')
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """функция, которая реагирует эхом на любое сообщение"""
    user = update.effective_user
    message = update.message
    log.info(f'Функция echo вызвана пользователем {user}\n' + ' ' * 73 + f'{message = }')
    await update.message.reply_text(f'{update.message.text}')


async def say_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Рассказывает, какие есть возможности у бота"""
    user = update.effective_user
    message = update.message
    log.info(f'Функция help вызвана пользователем {user}\n')

    text = [
        f'Привет, {user.first_name}!',
        '',
        'Я - школьный бот, который умеет реагировать на следующие команды:',
        '/hello - отвечаю приветствием',
        '/start /help - покажу список доступных команд',
        '/keyboard - покажу клавиатуру',
    ]
    text = '\n'.join(text)

    await update.message.reply_text(text)


async def say_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает inline-клавиатуру"""
    user = update.effective_user
    log.info(f'Функция say_keyboard вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Раз', callback_data='Раз'),
         InlineKeyboardButton('Два', callback_data='Два'),
         InlineKeyboardButton('Три', callback_data='Три')],
        [InlineKeyboardButton('Четыре', callback_data='Четыре'),
         InlineKeyboardButton('Пять', callback_data='Пять')],
        [InlineKeyboardButton('Шесть', callback_data='Шесть')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Выберите опцию на клавиатуре',
        reply_markup=keyboard
    )


async def react_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Реагирует на нажатие кнопки на inline-клавиатуре"""
    user = update.effective_user
    log.info(f'Функция react_keyboard вызвана пользователем {user}')

    query = update.callback_query

    if query.data == 'Раз':
        return await react_one(update, context)
    elif query.data == 'Два':
        return await react_two(update, context)
    elif query.data == 'Три':
        return await three(update, context)
    elif query.data == 'Четыре':
        return await four(update, context)
    elif query.data == 'Пять':
        return await five(update, context)
    elif query.data == 'Шесть':
        return await six(update, context)
    elif query.data == 'Городской транспорт':
        return await one_one(update, context)
    elif query.data == 'Водный транспорт':
        return await one_two(update, context)
    elif query.data == 'Информатика':
        return await two_one_answer(update, context)
    elif query.data == 'Физика':
        return await two_two_answer(update, context)


    buttons = [
        [InlineKeyboardButton('Раз', callback_data='Раз'),
         InlineKeyboardButton('Два', callback_data='Два'),
         InlineKeyboardButton('Три', callback_data='Три')],
        [InlineKeyboardButton('Четыре', callback_data='Четыре'),
         InlineKeyboardButton('Пять', callback_data='Пять')],
        [InlineKeyboardButton('Шесть', callback_data='Шесть')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=query.data,
        reply_markup=keyboard
    )

async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведет ответ на команду 'Раз'"""
    user = update.effective_user
    log.info(f'Функция one вызвана пользователем {user}\n')

    query = update.callback_query

    text = 'Машина'
    await query.edit_message_text(
        text=text
    )


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведет ответ на команду 'Два'"""
    user = update.effective_user
    log.info(f'Функция two вызвана пользователем {user}\n')

    query = update.callback_query

    text = 'Инторматика'
    await query.edit_message_text(
        text=text
    )


async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведет ответ на команду 'Три'"""
    user = update.effective_user
    log.info(f'Функция three вызвана пользователем {user}\n')

    query = update.callback_query

    text = 'Мотоцикл'
    await query.edit_message_text(
        text=text
    )


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведет ответ на команду 'Четыре'"""
    user = update.effective_user
    log.info(f'Функция four вызвана пользователем {user}\n')

    query = update.callback_query

    text = 'Кот'
    await query.edit_message_text(
        text=text
    )


async def five(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведет ответ на команду 'Пять'"""
    user = update.effective_user
    log.info(f'Функция four вызвана пользователем {user}\n')

    query = update.callback_query

    text = 'Бегемот'
    await query.edit_message_text(
        text=text
    )

async def six(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выведет ответ на команду 'Шесть'"""
    user = update.effective_user
    log.info(f'Функция four вызвана пользователем {user}\n')

    query = update.callback_query

    text = 'Ай-яй-яй'
    await query.edit_message_text(
        text=text
    )

async def say_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает inline-клавиатуру"""
    user = update.effective_user
    log.info(f'Функция say_one вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Городской транспорт', callback_data='Городской транспорт'),
         InlineKeyboardButton('Водный транспорт', callback_data='Водный транспорт')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Выберите опцию на клавиатуре',
        reply_markup=keyboard
    )
async def react_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Раз'"""
    user = update.effective_user
    log.info(f'Функция react_one вызвана пользователем {user}')

    query = update.callback_query



    buttons = [
        [InlineKeyboardButton('Городской транспорт', callback_data='Городской транспорт'),
         InlineKeyboardButton('Водный транспорт', callback_data='Водный транспорт')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text=query.data,
        reply_markup=keyboard
    )

async def one_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Городской транспорт'"""
    user = update.effective_user
    log.info(f'Функция one_one вызвана пользователем {user}')

    query = update.callback_query

    text = 'Машина'
    await query.edit_message_text(
        text=text
    )

async def one_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Волдный транспорт'"""
    user = update.effective_user
    log.info(f'Функция one_one вызвана пользователем {user}')

    query = update.callback_query

    text = 'Корабль'
    await query.edit_message_text(
        text=text
    )

async def say_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает inline-клавиатуру"""
    user = update.effective_user
    log.info(f'Функция say_two вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('Инфотрматика', callback_data='Инфотрматика'),
         InlineKeyboardButton('Физика', callback_data='Физика')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Какой школьный предмет изучает технологии?',
        reply_markup=keyboard
    )


async def react_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'inline-клавиатура'"""
    user = update.effective_user
    log.info(f'Функция react_two вызвана пользователем {user}')

    query = update.callback_query



    buttons = [
        [InlineKeyboardButton('Информатика', callback_data='Информатика'),
         InlineKeyboardButton('Физика', callback_data='Физика')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(
        text='Какой школьный предмет изучает технологии?',
        reply_markup=keyboard
    )

async def two_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Информатика'"""
    user = update.effective_user
    log.info(f'Функция two_one вызвана пользователем {user}')

    query = update.callback_query

    text = 'Информатика'
    await query.edit_message_text(
        text=text
    )


async def two_one_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Информатика'"""
    user = update.effective_user
    log.info(f'Функция two_one вызвана пользователем {user}')

    query = update.callback_query

    text = 'Правильно'
    await query.edit_message_text(
        text=text
    )

async def two_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Физика'"""
    user = update.effective_user
    log.info(f'Функция two_two вызвана пользователем {user}')

    query = update.callback_query

    text = 'Физика'
    await query.edit_message_text(
        text=text
    )

async def two_two_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Выдает ответ на кнопку 'Физика'"""
    user = update.effective_user
    log.info(f'Функция two_two вызвана пользователем {user}')

    query = update.callback_query

    text = 'Неправильно'
    await query.edit_message_text(
        text=text
    )

async def say_three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает inline-клавиатуру"""
    user = update.effective_user
    log.info(f'Функция say_three вызвана пользователем {user}')

    buttons = [
        [InlineKeyboardButton('', callback_data=''),
         InlineKeyboardButton('Физика', callback_data='Физика')]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text='Какой школьный предмет изучает технологии?',
        reply_markup=keyboard
    )

app = ApplicationBuilder().token(TOKEN).build()

# регистрация обработчиков
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler(["help", "start"], say_help))
app.add_handler(CommandHandler("keyboard", say_keyboard))
app.add_handler(CommandHandler("one", say_one))
app.add_handler(events_application_handler)
app.add_handler(CallbackQueryHandler(react_keyboard))
app.add_handler(MessageHandler(filters.ALL, echo))

app.run_polling()