from typing import Dict, Optional, List
from .binance import BinanceAPI
from .bybit import BybitAPI
import asyncio


class PriceComparator:
    def __init__(self):
        self.exchanges = {
            "binance": BinanceAPI(),
            "bybit": BybitAPI(),
        }

    async def compare_prices(self, symbol: str) -> List[Dict]:
        """Сравнить цены на всех биржах с подробной отладкой"""
        tasks = []
        exchange_names = []

        for name, exchange in self.exchanges.items():
            tasks.append(self._safe_get_price(exchange, symbol, name))
            exchange_names.append(name)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Отладочный вывод
        print(f"\n🔍 Результаты для {symbol}:")
        valid_results = []
        for name, result in zip(exchange_names, results):
            if isinstance(result, Exception):
                print(f"  ❌ {name}: Ошибка - {result}")
            elif result and result.get('price'):
                print(f"  ✅ {name}: ${result['price']:,.2f}")
                valid_results.append(result)
            else:
                print(f"  ⚠️  {name}: Нет данных")

        print(f"📊 Найдено валидных цен: {len(valid_results)}")

        # Сортируем по цене
        valid_results.sort(key=lambda x: x['price'])
        return valid_results

    async def _safe_get_price(self, exchange, symbol: str, exchange_name: str):
        """Безопасное получение цены с таймаутом"""
        try:
            # Добавляем таймаут для запроса
            return await asyncio.wait_for(exchange.get_price(symbol), timeout=10.0)
        except asyncio.TimeoutError:
            print(f"⏰ Таймаут для {exchange_name}")
            return None
        except Exception as e:
            print(f"❌ Ошибка в {exchange_name}: {e}")
            return None

    async def get_best_prices(self, symbol: str) -> Dict:
        """Найти лучшие цены"""
        prices = await self.compare_prices(symbol)

        if len(prices) == 0:
            return {"error": "Не удалось получить данные ни с одной биржи"}
        elif len(prices) == 1:
            return {
                "best_buy": prices[0],
                "best_sell": prices[0],
                "all_prices": prices,
                "spread": 0,
                "spread_percent": 0,
                "warning": "Данные только с одной биржи"
            }
        else:
            return {
                "best_buy": prices[0],
                "best_sell": prices[-1],
                "all_prices": prices,
                "spread": prices[-1]['price'] - prices[0]['price'],
                "spread_percent": ((prices[-1]['price'] - prices[0]['price']) / prices[0]['price']) * 100
            }

    async def get_multiple_prices(self, symbols: List[str]) -> Dict[str, Dict]:
        """Получить цены для нескольких криптовалют"""
        results = {}

        for symbol in symbols:
            print(f"\n🔄 Запрашиваю цены для {symbol}...")
            best_price = await self.get_best_prices(symbol)
            results[symbol] = best_price

            # Небольшая задержка между запросами чтобы не перегружать API
            await asyncio.sleep(0.5)

        return results

    async def debug_exchanges(self, symbol: str = "BTC"):
        """Подробная отладка всех бирж"""
        print(f"\n🐛 ОТЛАДКА БИРЖ ДЛЯ {symbol}:")
        for name, exchange in self.exchanges.items():
            print(f"\n🔧 Тестируем {name}...")
            try:
                result = await self._safe_get_price(exchange, symbol, name)
                if result:
                    print(f"   ✅ Успех: ${result['price']:,.2f}")
                else:
                    print(f"   ❌ Нет данных")
            except Exception as e:
                print(f"   💥 Критическая ошибка: {e}")