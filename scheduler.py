import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.constants import ParseMode
from utils.indicators import calculate_technical_indicators
from utils.analysis import generate_prediction_analysis, generate_news_analysis
from utils.report import generate_daily_report, generate_weekly_report, generate_monthly_report
from config import GROUP_CHAT_ID, CHANNEL_CHAT_ID
import matplotlib.pyplot as plt
import io
from telegram import InputFile

logger = logging.getLogger(__name__)

# 生成图表函数
async def generate_prediction_chart(prices, indicators):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(prices, label='价格', color='blue')

    ax2 = ax.twinx()
    ax2.plot(indicators['MACD'], label='MACD', color='green', linestyle='--')
    ax2.plot(indicators['RSI'], label='RSI', color='red', linestyle=':')

    ax.set_xlabel('时间')
    ax.set_ylabel('价格')
    ax2.set_ylabel('指标值')

    plt.title("BTC价格及技术指标预测")
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf

async def send_prediction_with_chart(application, prices, indicators):
    bot = application.bot
    chart = await generate_prediction_chart(prices, indicators)

    await bot.send_photo(
        chat_id=GROUP_CHAT_ID,
        photo=InputFile(chart, filename='prediction_chart.png'),
        caption="BTC价格及技术指标图表"
    )

async def send_hourly_prediction(application):
    bot = application.bot
    prices = [30000 + i for i in range(100)]
    indicators = calculate_technical_indicators(prices)

    analysis = generate_prediction_analysis(prices, indicators)
    prediction_direction = "上涨" if "上涨" in analysis else "下跌"

    message = f"""
📈 **【行情预测】BTC 下一小时**
- **预测方向**：{prediction_direction}
- **当前价格**：30000 USD
- **24小时变化**：+5%

🔍 **详细分析**：
{analysis}

🔗 [点击查看详细分析👉](https://yourwebsite.com/analysis)
    """

    await send_prediction_with_chart(application, prices, indicators)

    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message,
        parse_mode=ParseMode.MARKDOWN
    )

async def send_daily_report(update):
    report = generate_daily_report()
    await update.message.reply_document(InputFile(report, filename='daily_report.png'))

async def send_weekly_report(update):
    report = generate_weekly_report()
    await update.message.reply_document(InputFile(report, filename='weekly_report.png'))

async def send_monthly_report(update):
    report = generate_monthly_report()
    await update.message.reply_document(InputFile(report, filename='monthly_report.png'))

def setup_scheduler(application):
    scheduler = AsyncIOScheduler()
    from pytz import timezone
    tz = timezone('Asia/Shanghai')

    scheduler.add_job(send_hourly_prediction, 'cron', minute=0, args=[application], timezone=tz)
    scheduler.add_job(send_daily_report, 'cron', hour=10, minute=0, args=[application], timezone=tz)
    scheduler.add_job(send_weekly_report, 'cron', day_of_week='sun', hour=10, minute=0, args=[application], timezone=tz)
    scheduler.add_job(send_monthly_report, 'cron', day=1, hour=10, minute=0, args=[application], timezone=tz)

    scheduler.start()

