import aiohttp
import json
from typing import Dict, Optional


class BinanceAPI:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3"
        self.name = "Binance"

    async def get_price(self, symbol: str) -> Optional[Dict]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/ticker/price?symbol={symbol}USDT") as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'exchange': self.name,
                            'symbol': symbol,
                            'price': float(data['price']),
                            'volume': None
                        }
        except Exception as e:
            print(f"Error fetching Binance price for {symbol}: {e}")
            return None
