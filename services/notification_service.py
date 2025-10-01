import asyncio
import sqlite3
from typing import Dict, List
from models.notifications import PriceAlert


class NotificationService:
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS price_alerts
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER NOT NULL,
                           symbol TEXT NOT NULL,
                           target_price REAL NOT NULL,
                           condition TEXT NOT NULL,
                           is_active BOOLEAN DEFAULT TRUE,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           last_triggered TIMESTAMP 
                       )
                       """)

        conn.commit()
        conn.close()

    def __init__(self, db_path: str, bot):
        self.db_path = db_path
        self.bot = bot
        self.is_running = False
        self._init_db()

    async def add_alert(self, user_id: int, symbol: str, target_price: float, condition: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO price_alerts (user_id, symbol, target_price, condition)
                VALUES (?, ?, ?, ?)
            """, (user_id, symbol.upper(), target_price, condition))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"Error adding alert: {e}")
            return False

    async def get_user_alerts(self, user_id: int) -> List[PriceAlert]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM price_alerts
            WHERE user_id = ? AND is_active = TRUE
            ORDER by created_at DESC  
        """, (user_id,))

        alerts = []
        for row in cursor.fetchall():
            alerts.append(PriceAlert(
                id=row[0], user_id=row[1], symbol=row[2],
                target_price=row[3], condition=row[4],
                is_active=bool(row[5]), created_at=row[6],
                last_triggered=row[7]
            ))

        conn.close()
        return alerts

    async def check_alerts(self, symbol: str, current_price: float):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
                       SELECT *
                       FROM price_alerts
                       WHERE symbol = ?
                         AND is_active = TRUE
                       ''', (symbol.upper(),))

        for row in cursor.fetchall():
            alert = PriceAlert(
                id=row[0], user_id=row[1], symbol=row[2],
                target_price=row[3], condition=row[4],
                is_active=bool(row[5]), created_at=row[6],
                last_triggered=row[7]
            )

            should_trigger = False
            message = ""

            if alert.condition == "above" and current_price >= alert.target_price:
                should_trigger = True
                message = f"🚀 {symbol} достигла целевой цены ${alert.target_price:,.2f}!"

            elif alert.condition == "below" and current_price <= alert.target_price:
                should_trigger = True
                message = f"📉 {symbol} упала ниже ${alert.target_price:,.2f}!"

            if should_trigger:
                await self._trigger_alert(alert, message, current_price)





