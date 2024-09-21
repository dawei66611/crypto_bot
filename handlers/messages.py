# handlers/messages.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.report import generate_daily_report, generate_weekly_report, generate_monthly_report, plot_report
import logging

logger = logging.getLogger(__name__)

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()

    if "今日报表" in message:
        await send_daily_report(update)
    elif "周报表" in message:
        await send_weekly_report(update)
    elif "月报表" in message:
        await send_monthly_report(update)
    else:
        await update.message.reply_text("抱歉，我不明白您的意思。您可以输入“今日报表”、“周报表”或“月报表”来获取相关报表。")

async def send_daily_report(update: Update):
    try:
        df = generate_daily_report()
        chart = plot_report(df, "每日预测报表")
        await update.message.reply_photo(photo=chart, caption="您的每日预测报表。")
    except Exception as e:
        logger.error(f"发送每日报表失败: {e}")
        await update.message.reply_text("生成每日报表时出错，请稍后再试。")

async def send_weekly_report(update: Update):
    try:
        df = generate_weekly_report()
        chart = plot_report(df, "每周预测报表")
        await update.message.reply_photo(photo=chart, caption="您的每周预测报表。")
    except Exception as e:
        logger.error(f"发送周报表失败: {e}")
        await update.message.reply_text("生成周报表时出错，请稍后再试。")

async def send_monthly_report(update: Update):
    try:
        df = generate_monthly_report()
        chart = plot_report(df, "每月预测报表")
        await update.message.reply_photo(photo=chart, caption="您的每月预测报表。")
    except Exception as e:
        logger.error(f"发送月报表失败: {e}")
        await update.message.reply_text("生成月报表时出错，请稍后再试。")
