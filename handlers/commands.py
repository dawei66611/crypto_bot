# handlers/commands.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.db import (
    update_user_membership,
    verify_activation_code,
    mark_activation_code_as_used,
    get_referral_code,
    set_referral
)
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    referral_code = await get_referral_code(user_id)
    message = (
        "欢迎使用加密货币助手！\n"
        "输入 /activate <激活码> 激活会员功能。\n"
        f"您的推荐码：{referral_code}\n"
        "邀请好友使用您的推荐码，您和您的好友都将获得奖励！"
    )
    await update.message.reply_text(message)

async def activate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("请输入激活码：/activate <激活码>")
        return

    code = args[0]
    user_id = update.message.from_user.id

    try:
        if await verify_activation_code(code):
            # 更新会员等级并设置会员时长
            await update_user_membership(user_id, level="初级会员", add_days=30)
            await mark_activation_code_as_used(code)
            await update.message.reply_text("激活成功！您已成为初级会员，享受30天会员期。")
        else:
            await update.message.reply_text("无效的激活码，请联系管理员获取有效的激活码。")
    except Exception as e:
        logger.error(f"激活码验证失败: {e}")
        await update.message.reply_text("激活过程中出现错误，请稍后再试。")

async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    referral_code = await get_referral_code(user_id)
    invite_link = f"https://t.me/YourBotUsername?start={referral_code}"
    await update.message.reply_text(f"邀请好友使用您的推荐码：{referral_code}\n邀请链接：{invite_link}")
