# handlers/images.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.ocr import perform_ocr
import logging

logger = logging.getLogger(__name__)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        image_file = await photo.get_file()
        image_data = await image_file.download_as_bytearray()
        text = perform_ocr(image_data)
        if text.strip():
            await update.message.reply_text(f"识别到的文字：\n{text}")
        else:
            await update.message.reply_text("未能识别到文字。")
    except Exception as e:
        logger.error(f"OCR 处理失败: {e}")
        await update.message.reply_text("处理图片时出错，请稍后再试。")
