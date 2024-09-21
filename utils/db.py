# utils/db.py

import aiosqlite
from datetime import datetime, timedelta
from config import DATABASE, VALID_ACTIVATION_CODES
import uuid
import asyncio

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                membership_level TEXT,
                subscription_end DATETIME,
                referral_code TEXT,
                referred_by INTEGER
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS activation_codes (
                code TEXT PRIMARY KEY,
                is_used INTEGER DEFAULT 0
            )
        ''')
        for code in VALID_ACTIVATION_CODES:
            await db.execute('INSERT OR IGNORE INTO activation_codes (code) VALUES (?)', (code,))
        await db.commit()

async def verify_activation_code(code):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT is_used FROM activation_codes WHERE code=?', (code,)) as cursor:
            result = await cursor.fetchone()
            if result and result[0] == 0:
                return True
            return False

async def mark_activation_code_as_used(code):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('UPDATE activation_codes SET is_used=1 WHERE code=?', (code,))
        await db.commit()

async def update_user_membership(user_id, level, add_days):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT subscription_end FROM users WHERE telegram_id=?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result and result[0]:
                current_end = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
                new_end = current_end + timedelta(days=add_days)
            else:
                new_end = datetime.now() + timedelta(days=add_days)
        await db.execute('''
            INSERT INTO users (telegram_id, membership_level, subscription_end)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                membership_level=excluded.membership_level,
                subscription_end=excluded.subscription_end
        ''', (user_id, level, new_end.strftime('%Y-%m-%d %H:%M:%S')))
        await db.commit()

async def get_membership_level(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT membership_level, subscription_end FROM users WHERE telegram_id=?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                level, end_time = result
                if datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
                    return level
        return None

def generate_referral_code():
    return uuid.uuid4().hex[:8]

async def get_referral_code(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT referral_code FROM users WHERE telegram_id=?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result and result[0]:
                return result[0]
            referral_code = generate_referral_code()
            await db.execute('UPDATE users SET referral_code=? WHERE telegram_id=?', (referral_code, user_id))
            await db.commit()
            return referral_code

async def set_referral(user_id, referrer_id):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            UPDATE users SET referred_by=? WHERE telegram_id=?
        ''', (referrer_id, user_id))
        await db.commit()
