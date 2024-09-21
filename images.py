# handlers/images.py
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils.db import get_membership_level
from utils.ocr import extract_text_from_image, parse_profit_loss_text
import logging

logger = logging.getLogger(__name__)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理用户发送的图片消息，执行OCR并分析内容
    """
    user_id = update.effective_user.id
    membership_level = get_membership_level(user_id)
    
    if not membership_level:
        await update.message.reply_text("🎉 新用户欢迎！请联系管理员领取激活码以体验初级会员权限。")
        return
    
    # 获取图片文件
    try:
        photo = update.message.photo[-1]  # 获取最高分辨率的图片
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()
    except Exception as e:
        logger.error(f"获取图片失败: {e}")
        await update.message.reply_text("❌ 无法获取您发送的图片。请稍后再试。")
        return
    
    # 执行OCR
    extracted_text = extract_text_from_image(image_bytes)
    if not extracted_text:
        await update.message.reply_text("❌ 无法从图片中提取文本。请确保截图清晰并包含相关信息。")
        return
    
    # 解析内容（示例：盈利或亏损）
    profit, loss = parse_profit_loss_text(extracted_text)
    
    # 生成反馈
    if profit > 0:
        message = f"🎉 恭喜您！本次交易盈利 **+{profit} USDT**。"
    elif loss > 0:
        message = f"⚠️ 注意！本次交易亏损 **-{loss} USDT**。"
    else:
        message = "ℹ️ 我已收到您的图片，但未能识别具体内容。如有问题，请直接发送文字信息。"
    
    await update.message.reply_text(message)
