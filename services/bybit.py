import aiohttp
import json
from typing import Dict, Optional


class BybitAPI:
    def __init__(self):
        self.base_url = "https://api.bybit.com"
        self.name = "Bybit"

    async def get_price(self, symbol: str) -> Optional[Dict]:
        """Пробуем разные версии API Bybit"""

        # Сначала пробуем v5 API
        result = await self._try_v5_api(symbol)
        if result:
            return result

        # Если v5 не сработал, пробуем v2 API
        result = await self._try_v2_api(symbol)
        if result:
            return result

        print(f"Все API Bybit не сработали для {symbol}")
        return None

    async def _try_v5_api(self, symbol: str) -> Optional[Dict]:
        """Попробовать v5 API"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/v5/market/tickers"
                params = {"category": "spot", "symbol": f"{symbol}USDT"}

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('retCode') == 0 and data.get('result'):
                            tickers = data['result'].get('list', [])
                            if tickers:
                                ticker = tickers[0]
                                return {
                                    'exchange': self.name,
                                    'symbol': symbol,
                                    'price': float(ticker['lastPrice']),
                                    'volume': float(ticker.get('volume24h', 0)),
                                    'timestamp': ticker.get('time', None)
                                }
        except Exception as e:
            print(f"Bybit v5 API error for {symbol}: {e}")
        return None

    async def _try_v2_api(self, symbol: str) -> Optional[Dict]:
        """Попробовать v2 API"""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.bybit.com/v2/public/tickers"
                params = {"symbol": f"{symbol}USDT"}

                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('result'):
                            tickers = data['result']
                            if tickers:
                                ticker = tickers[0]
                                return {
                                    'exchange': self.name,
                                    'symbol': symbol,
                                    'price': float(ticker['last_price']),
                                    'volume': float(ticker.get('volume', 0)),
                                    'timestamp': ticker.get('time', None)
                                }
        except Exception as e:
            print(f"Bybit v2 API error for {symbol}: {e}")
        return None
