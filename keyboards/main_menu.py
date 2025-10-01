from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    buttons = [
        KeyboardButton(text="📊 Проверить цену"),
        KeyboardButton(text="⭐ Избранное"),
        KeyboardButton(text="📈 Топ криптовалют"),
        KeyboardButton(text="📰 Новости"),
        KeyboardButton(text="⚙️ Настройки"),
        KeyboardButton(text="ℹ️ Помощь")
    ]

    for button in buttons:
        builder.add(button)

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def crypto_menu() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    cryptos = [
        "BTC", "ETH", "BNB", "SOL", "XRP",
        "ADA", "AVAX", "DOT", "DOGE", "MATIC"
    ]

    for crypto in cryptos:
        builder.add(KeyboardButton(text=crypto))

    builder.add(KeyboardButton(text="↩️ Назад"))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


def back_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="↩️ Назад"))
    return builder.as_markup(resize_keyboard=True)