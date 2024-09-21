from telegram import Update
from telegram.ext import ContextTypes

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_path = file.file_path
    # 示例：你可以将图片下载后处理，或者直接回应用户
    await update.message.reply_text(f"已收到图片，文件路径为: {file_path}")

