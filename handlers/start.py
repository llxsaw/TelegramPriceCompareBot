from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards.main_menu import main_menu
from services.price_comparator import PriceComparator

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = """
🚀 *Добро пожаловать в Crypto Monitor Bot!*

Я помогу вам отслеживать цены на криптовалюты на различных биржах!

📊 *Основные функции:*
• Сравнение цен на разных биржах
• Поиск лучших цен для покупки/продажи
• Отслеживание избранных криптовалют

Выберите действие из меню ниже 👇
"""
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=main_menu())


@router.message(Command("help"))
@router.message(F.text == "ℹ️ Помощь")
async def cmd_help(message: Message):
    text = """
ℹ️ *Помощь по командам:*

/start - Запустить бота
/price - Проверить цену криптовалюты
/top - Показать топ криптовалют
/help - Показать эту справку

📊 *Используйте кнопки меню для удобной навигации!*
"""
    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu())


@router.message(Command("test"))
async def test_exchanges(message: Message):
    """Тестовая команда для проверки всех бирж"""
    comparator = PriceComparator()

    # Тестируем BTC
    await comparator.debug_exchanges("BTC")

    # Получаем цены
    best_price = await comparator.get_best_prices("BTC")

    if best_price.get("error"):
        response = f"❌ {best_price['error']}"
    else:
        response = f"✅ Тест завершен!\n"
        response += f"📊 Получено цен: {len(best_price['all_prices'])}\n"
        response += f"🏪 Биржи: {', '.join([p['exchange'] for p in best_price['all_prices']])}"

    await message.answer(response)
