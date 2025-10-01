def format_price_comparison(symbol: str, data: dict) -> str:
    if not data:
        return "❌ Не удалось получить данные"

    # Проверяем наличие ошибки
    if data.get("error"):
        return f"❌ {data['error']} для {symbol}"

    # Проверяем наличие предупреждения
    warning_text = ""
    if data.get("warning"):
        warning_text = f"\n⚠️ *Примечание:* {data['warning']}\n"

    best_buy = data['best_buy']
    best_sell = data['best_sell']

    text = f"📊 *{symbol}/USDT* - Сравнение цен\n\n"
    text += f"🛒 *Лучшая цена для покупки:*\n"
    text += f"   • {best_buy['exchange']}: `${best_buy['price']:,.2f}`\n\n"
    text += f"💰 *Лучшая цена для продажи:*\n"
    text += f"   • {best_sell['exchange']}: `${best_sell['price']:,.2f}`\n\n"

    # Добавляем спред только если есть разница в ценах
    if data.get('spread', 0) > 0:
        text += f"📈 *Спред:* `${data['spread']:,.4f}` "
        text += f"(*{data['spread_percent']:.2f}%*)\n\n"

    text += "*Все цены:*\n"

    for price_data in data['all_prices']:
        if len(data['all_prices']) == 1:
            emoji = "⚪"  # Если только одна цена
        else:
            emoji = "🟢" if price_data == best_buy else "🔴" if price_data == best_sell else "⚪"

        text += f"{emoji} {price_data['exchange']}: `${price_data['price']:,.2f}`\n"

    text += warning_text
    text += f"\n⏰ *Обновлено:* {data['all_prices'][0].get('timestamp', 'N/A')}"
    return text


def format_multiple_prices(data: dict) -> str:
    """Форматирование цен для нескольких криптовалют"""
    if not data:
        return "❌ Не удалось получить данные"

    text = "📈 *Топ криптовалют - текущие цены*\n\n"

    successful = 0
    for symbol, price_data in data.items():
        if price_data and not price_data.get("error") and price_data.get("best_buy"):
            best_price = price_data['best_buy']['price']
            exchange = price_data['best_buy']['exchange']
            text += f"• **{symbol}**: `${best_price:,.2f}` ({exchange})\n"
            successful += 1
        else:
            text += f"• **{symbol}**: ❌ Нет данных\n"

    text += f"\n✅ Успешно загружено: {successful}/{len(data)}"
    text += "\n\n💡 Используйте *Проверить цену* для детального сравнения"

    return text