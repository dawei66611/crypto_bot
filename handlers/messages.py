from telegram.constants import ParseMode
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from utils.report import generate_daily_report, generate_weekly_report, generate_monthly_report, plot_report

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()

    if "今日报表" in message:
        await send_daily_report(update)
    elif "周报表" in message:
        await send_weekly_report(update)
    elif "月报表" in message:
        await send_monthly_report(update)
    else:
        return

async def send_daily_report(update: Update):
    df = generate_daily_report()
    chart = plot_report(df, "每日预测报表")
    await update.message.reply_photo(photo=InputFile(chart, filename='daily_report.png'))

async def send_weekly_report(update: Update):
    df = generate_weekly_report()
    chart = plot_report(df, "每周预测报表")
    await update.message.reply_photo(photo=InputFile(chart, filename='weekly_report.png'))

async def send_monthly_report(update: Update):
    df = generate_monthly_report()
    chart = plot_report(df, "每月预测报表")
    await update.message.reply_photo(photo=InputFile(chart, filename='monthly_report.png'))

