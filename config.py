import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS_ID = list(map(int, os.getenv("ADMINS_ID", '').split(','))) if os.getenv("ADMINS_ID") else []

DB_PATH = os.getenv("DB_PATH")

EXCHANGES = ['binance', 'bybit', 'kucoin', 'huobi', 'okx']
DEFAULT_CRYPTOS = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOT', 'DOGE', 'AVAX', 'MATIC']

CRYPTO_PANIC_API = os.getenv("CRYPTO_PANIC_API")
