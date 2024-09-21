# handlers/commands.py
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils.db import (
    verify_activation_code,
    mark_activation_code_as_used,
    update_user_membership,
    get_membership_level,
    get_referral_code
)
from utils.analysis import generate_prediction_analysis
from utils.indicators import calculate_technical_indicators
from utils.analysis import generate_news_analysis
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /start 命令
    """
    user_id = update.effective_user.id
    membership_level = get_membership_level(user_id)
    
    if membership_level == 'premium':
        # 获取最新数据
        news = "示例新闻摘要"  # 实际应调用fetch_latest_news()
        price = 30000  # 实际应调用fetch_current_price()
        change_24h = 5.0  # 实际应调用fetch_current_price()
        indicators = {
            "MACD": 0.5,
            "MACD_Signal": 0.4,
            "RSI": 60.0
        }  # 实际应调用calculate_technical_indicators()
        
        analysis = generate_prediction_analysis(news, price, change_24h, indicators)
        await update.message.reply_text(analysis, parse_mode=ParseMode.MARKDOWN)
    
    elif membership_level == 'basic':
        # 发送简单预测方向
        prediction_direction = "上涨"  # 实际应调用get_prediction_direction()
        await update.message.reply_text(f"预测方向：**{prediction_direction}**", parse_mode=ParseMode.MARKDOWN)
    
    else:
        await update.message.reply_text("🎉 新用户欢迎！请联系管理员领取激活码以体验初级会员权限。")

async def activate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /activate <code> 命令
    """
    user_id = update.effective_user.id
    activation_code = ' '.join(context.args).strip().upper()
    
    if not activation_code:
        await update.message.reply_text("❌ 请输入激活码。使用命令：`/activate <激活码>`", parse_mode=ParseMode.MARKDOWN)
        return
    
    if verify_activation_code(activation_code):
        mark_activation_code_as_used(activation_code)
        update_user_membership(user_id, 'basic', add_days=7)
        await update.message.reply_text("🎉 激活成功！您已获得7日基础会员权限，可以查看预测方向。")
    else:
        await update.message.reply_text("❌ 激活码无效或已使用。请联系管理员获取有效的激活码。")

async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    处理 /invite 命令，发送用户的推荐链接
    """
    user_id = update.effective_user.id
    referral_code = get_referral_code(user_id)
    referral_link = f"https://yourwebsite.com/register?ref={referral_code}&utm_source=telegram&utm_medium=bot&utm_campaign=invite"
    await update.message.reply_text(
        f"📢 邀请您的好友注册智链AI交易Bot，获取更多奖励！点击链接分享👉 [邀请链接]({referral_link})",
        parse_mode=ParseMode.MARKDOWN
    )
