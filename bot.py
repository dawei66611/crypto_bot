import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from handlers import (
    start_command,
    activate_command,
    invite_command,
    handle_text_message,
    handle_image
)
from utils.db import init_db
from scheduler import setup_scheduler

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    # 初始化数据库
    init_db()

    # 创建Telegram应用
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # 添加命令处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("activate", activate_command))
    application.add_handler(CommandHandler("invite", invite_command))

    # 添加消息处理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # 添加图片处理器
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # 注册定时任务
    setup_scheduler(application)

    # 启动Bot
    application.run_polling()

if __name__ == '__main__':
    main()

