from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from services.notification_service import NotificationService
from keyboards.notifications import get_alerts_keyboard

router = Router()


class AlertStates(StatesGroup):
    choosing_symbol = State()
    choosing_condition = State()
    entering_price = State()


@router.message(Command("alerts"))
@router.message(F.text == "🔔 Уведомления")
async def alerts_command(message: Message, state: FSMContext):
    text = """
🔔 *Управление уведомлениями*

Здесь вы можете настроить уведомления о достижении цен:

• 📈 Уведомить когда цена ВЫШЕ целевой
• 📉 Уведомить когда цена НИЖЕ целевой
• 📊 Просмотреть активные уведомления

Выберите действие:
    """
    await message.answer(text, parse_mode="Markdown", reply_markup=get_alerts_keyboard())


@router.message(F.text == "📈 Добавить уведомление")
async def add_alerts_start(message: Message, state: FSMContext):
    await message.answer("Введите символ криптовалюты (например BTC):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AlertStates.choosing_symbol)


@router.message(AlertStates.choosing_symbol)
async def alert_symbol_chosen(message: Message, state: FSMContext):
    symbol = message.text.upper()
    await state.update_data(symbol=symbol)
    text = f"""
Выбран: {symbol}

Выберите условие уведомления:
• 📈 Уведомить когда цена ВЫШЕ целевой
• 📉 Уведомить когда цена НИЖЕ целевой
    """

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📈 Выше целевой"), KeyboardButton(text="📉 Ниже целевой"),
             KeyboardButton(text="↩️ Отмена")],
        ],
        resize_keyboard=True,
    )
    await message.answer(text, reply_markup=keyboard)
    await state.set_state(AlertStates.choosing_condition)


@router.message(AlertStates.choosing_condition, F.text.in_(["📈 Выше целевой", "📉 Ниже целевой"]))
async def alert_condition_chosen(message: Message, state: FSMContext):
    condition = "above" if "Выше" in message.text else "below"
    await state.update_data(condition=condition)

    condition_text = "выше" if condition == "above" else "ниже"
    data = await state.get_data()
    symbol = data['symbol']

    await message.answer(
        f"Введите целевую цену для {symbol} (уведомление сработает когда цена будет {condition_text} этой):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AlertStates.entering_price)


@router.message(AlertStates.entering_price)
async def alert_price_entered(message: Message, state: FSMContext):
    try:
        target_price = float(message.text)
        data = await state.get_data()
        notification_service = NotificationService("crypto_bot.db", message.bot)
        success = await notification_service.add_alert(
            message.from_user.id,
            data["symbol"],
            target_price,
            data["condition"],
        )
        if success:
            condition_text = "выше" if data["condition"] == "above" else "ниже"
            await message.answer(
                f"✅ Уведомление для {data['symbol']} установлено!\n"
                f"🔔 Сработает когда цена будет {condition_text} ${target_price:,.2f}",
                reply_markup=get_alerts_keyboard()
            )
        else:
            await message.answer("❌ Ошибка при создании уведомления")

    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную цену (например: 50000.50")
        return
    await state.clear()


@router.message(F.text == "📋 Мои уведомления")
async def show_alerts(message: Message, state: FSMContext):
    notification_service = NotificationService("crypto_bot.db", message.bot)
    alerts = await notification_service.get_user_alerts(message.from_user.id)

    if not alerts:
        await message.answer("📭 У вас нет активных уведомлений")
        return
    text = "📋 *Ваши активные уведомления:*\n\n"
    for alert in alerts:
        condition_emoji = "📈" if alert.condition == "above" else "📉"
        condition_text = "выше" if alert.condition == "above" else "ниже"
        text += f"{condition_emoji} {alert.symbol}: {condition_text} ${alert.target_price:,.2f}\n"

    await message.answer(text, parse_mode="Markdown")
