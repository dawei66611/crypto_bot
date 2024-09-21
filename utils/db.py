import sqlite3
from datetime import datetime, timedelta
from config import DATABASE, VALID_ACTIVATION_CODES
import uuid

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            membership_level TEXT,
            subscription_end DATETIME,
            referral_code TEXT,
            referred_by INTEGER
        )
    ''')
    # 创建激活码表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activation_codes (
            code TEXT PRIMARY KEY,
            is_used INTEGER DEFAULT 0
        )
    ''')
    # 插入有效激活码
    for code in VALID_ACTIVATION_CODES:
        cursor.execute('INSERT OR IGNORE INTO activation_codes (code) VALUES (?)', (code,))
    conn.commit()
    conn.close()

def verify_activation_code(code):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT is_used FROM activation_codes WHERE code=?', (code,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == 0:
        return True
    return False

def mark_activation_code_as_used(code):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE activation_codes SET is_used=1 WHERE code=?', (code,))
    conn.commit()
    conn.close()

def update_user_membership(user_id, level, add_days):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_end FROM users WHERE telegram_id=?', (user_id,))
    result = cursor.fetchone()
    if result and result[0]:
        current_end = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        new_end = current_end + timedelta(days=add_days)
    else:
        new_end = datetime.now() + timedelta(days=add_days)
    cursor.execute('''
        INSERT INTO users (telegram_id, membership_level, subscription_end)
        VALUES (?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
            membership_level=excluded.membership_level,
            subscription_end=excluded.subscription_end
    ''', (user_id, level, new_end.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def get_membership_level(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT membership_level, subscription_end FROM users WHERE telegram_id=?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        level, end_time = result
        if datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
            return level
    return None

def generate_referral_code():
    return uuid.uuid4().hex[:8]

def get_referral_code(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT referral_code FROM users WHERE telegram_id=?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]:
        return result[0]
    return generate_referral_code()

def set_referral(user_id, referrer_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET referred_by=? WHERE telegram_id=?
    ''', (referrer_id, user_id))
    conn.commit()
    conn.close()

