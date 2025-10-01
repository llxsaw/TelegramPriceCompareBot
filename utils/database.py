import sqlite3
import json
from datetime import datetime


class NotificationManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            target_price REAL NOT NULL,
            condition TEXT NOT NULL, -- 'above', 'below', 'change'
            is_active BOOLEAN DEFAULT  TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_triggered TIMESTAMP NULL,
            )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            notification_enabled BOOLEAN DEFAULT TRUE,
            language TEXT DEFAULT 'ru',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        """)

        conn.commit()
        conn.close()
