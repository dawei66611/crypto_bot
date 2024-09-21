from telegram import Update
from telegram.ext import ContextTypes
from utils.db import update_user_membership, verify_activation_code, mark_activation_code_as_used

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎使用加密货币助手！输入 /activate 激活会员功能。")

async def activate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("请输入激活码：/activate <激活码>")
        return

    code = args[0]
    user_id = update.message.from_user.id

    if verify_activation_code(code):
        # 更新会员等级并设置会员时长
        update_user_membership(user_id, level="初级会员", add_days=30)
        mark_activation_code_as_used(code)
        await update.message.reply_text("激活成功！您已成为初级会员，享受30天会员期。")
    else:
        await update.message.reply_text("无效的激活码，请联系管理员获取有效的激活码。")

