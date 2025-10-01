from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from keyboards.main_menu import main_menu, crypto_menu
from services.price_comparator import PriceComparator
from utils.formatters import format_price_comparison, format_multiple_prices
from config import DEFAULT_CRYPTOS

router = Router()


class PriceStates(StatesGroup):
    choosing_crypto = State()


@router.message(Command("price"))
@router.message(F.text == "📊 Проверить цену")
async def price_command(message: Message, state: FSMContext):
    await message.answer(
        "Выберите криптовалюту:",
        reply_markup=crypto_menu()
    )
    await state.set_state(PriceStates.choosing_crypto)


@router.message(PriceStates.choosing_crypto, F.text.in_({
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP',
    'ADA', 'AVAX', 'DOT', 'DOGE', 'MATIC'
}))
async def crypto_selected(message: Message, state: FSMContext):
    crypto = message.text
    await message.answer(f"🔍 Запрашиваю цены для {crypto}...")

    comparator = PriceComparator()
    best_price = await comparator.get_best_prices(crypto)

    if not best_price:
        await message.answer("❌ Не удалось получить данные. Попробуйте позже.")
        await state.clear()
        return

    response = format_price_comparison(crypto, best_price)
    await message.answer(response, parse_mode="Markdown", reply_markup=main_menu())
    await state.clear()


@router.message(PriceStates.choosing_crypto, F.text == "↩️ Назад")
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню:", reply_markup=main_menu())


@router.message(Command("top"))
@router.message(F.text == "📈 Топ криптовалют")
async def top_cryptos(message: Message):
    await message.answer("🔄 Загружаю актуальные цены...")

    comparator = PriceComparator()
    top_symbols = DEFAULT_CRYPTOS
    prices = await comparator.get_multiple_prices(top_symbols)

    response = format_multiple_prices(prices)
    await message.answer(response, parse_mode="Markdown", reply_markup=main_menu())