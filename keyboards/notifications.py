from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_alerts_keyboard():
    keyboard = [
        [KeyboardButton(text="📈 Добавить уведомление")],
        [KeyboardButton(text="📋 Мои уведомления")],
        [KeyboardButton(text="↩️ Главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

