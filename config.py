# config.py

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
CMC_API_KEY = os.getenv('CMC_API_KEY')
GROUP_CHAT_ID = int(os.getenv('GROUP_CHAT_ID', '0'))
CHANNEL_CHAT_ID = int(os.getenv('CHANNEL_CHAT_ID', '0'))
DATABASE = os.getenv('DATABASE', 'bot_database.db')

# GPT模型名称
GPT_MODEL = "gpt-4"

# 有效激活码列表（可在 .env 中配置）
VALID_ACTIVATION_CODES = os.getenv('VALID_ACTIVATION_CODES', '').split(',')
