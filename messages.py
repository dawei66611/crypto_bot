# handlers/messages.py
from telegram.constants import ParseMode
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from utils.report import generate_daily_report, generate_weekly_report, generate_monthly_report

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理文本消息，针对特定关键词响应
    """
    message = update.message.text.lower()

    # 关键词触发条件
    if "今日报表" in message:
        await send_daily_report(update)
    elif "周报表" in message:
        await send_weekly_report(update)
    elif "月报表" in message:
        await send_monthly_report(update)
    else:
        # 忽略不相关消息
        return

async def send_daily_report(update: Update):
    """
    发送今日报表图片
    """
    image_path = generate_daily_report()
    with open(image_path, 'rb') as img:
        await update.message.reply_photo(photo=InputFile(img), caption="📊 **今日报表**")

async def send_weekly_report(update: Update):
    """
    发送周报表图片
    """
    image_path = generate_weekly_report()
    with open(image_path, 'rb') as img:
        await update.message.reply_photo(photo=InputFile(img), caption="📊 **周报表**")

async def send_monthly_report(update: Update):
    """
    发送月报表图片
    """
    image_path = generate_monthly_report()
    with open(image_path, 'rb') as img:
        await update.message.reply_photo(photo=InputFile(img), caption="📊 **月报表**")
