# scheduler.py

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from utils.indicators import calculate_technical_indicators
from utils.analysis import generate_prediction_analysis, generate_news_analysis
from utils.market_data import fetch_cmc_market_data
from utils.news import fetch_latest_news
from utils.gpt_analysis import generate_gpt_analysis
from config import GROUP_CHAT_ID
from telegram import InputFile, ParseMode
import matplotlib.pyplot as plt
import io

logger = logging.getLogger(__name__)

async def send_prediction_with_chart(application, prices, indicators):
    try:
        bot = application.bot
        chart = await generate_prediction_chart(prices, indicators)

        await bot.send_photo(
            chat_id=GROUP_CHAT_ID,
            photo=InputFile(chart, filename='prediction_chart.png'),
            caption="BTC价格及技术指标图表"
        )
    except Exception as e:
        logger.error(f"发送图表失败: {e}")

async def generate_prediction_chart(prices, indicators):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(prices, label='价格', color='blue')

    # 绘制技术指标
    macd = indicators['MACD']
    rsi = indicators['RSI']
    boll_upper = indicators['Bollinger_Upper']
    boll_middle = indicators['Bollinger_Middle']
    boll_lower = indicators['Bollinger_Lower']

    ax.plot(prices, label='价格', color='blue')
    ax.plot([boll_upper]*len(prices), label='Bollinger Upper', color='green', linestyle='--')
    ax.plot([boll_middle]*len(prices), label='Bollinger Middle', color='orange', linestyle='--')
    ax.plot([boll_lower]*len(prices), label='Bollinger Lower', color='green', linestyle='--')

    ax2 = ax.twinx()
    ax2.plot([macd]*len(prices), label='MACD', color='purple', linestyle='-.')
    ax2.plot([rsi]*len(prices), label='RSI', color='red', linestyle=':')

    ax.set_xlabel('时间')
    ax.set_ylabel('价格 (USD)')
    ax2.set_ylabel('指标值')

    plt.title("BTC价格及技术指标预测")
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

async def send_hourly_prediction(application):
    try:
        bot = application.bot
        # 获取实时价格
        current_price = await fetch_cmc_market_data('BTC')
        # 示例历史价格，实际应从 API 获取
        # 这里假设过去100小时的价格，每小时递减100美元作为示例
        prices = [current_price - i * 100 for i in range(100)][::-1]
        indicators = calculate_technical_indicators(prices)

        # 获取最新新闻
        news = await fetch_latest_news('Bitcoin')
        news_analysis = generate_news_analysis(news)

        # 生成详细分析报告
        gpt_analysis = await generate_gpt_analysis(indicators, news_analysis)

        # 构建预测方向
        prediction_direction = "上涨" if "上涨" in gpt_analysis else "下跌"

        # 构建消息
        change_percent = ((current_price - prices[-1]) / prices[-1]) * 100
        message = f"""
📈 **【行情预测】BTC 下一小时**
- **预测方向**：{prediction_direction}
- **当前价格**：{current_price:.2f} USD
- **24小时变化**：{change_percent:.2f}%

🔍 **详细分析**：
{gpt_analysis}

🔗 [点击查看详细分析👉](https://yourwebsite.com/analysis)
        """

        # 生成并发送图表
        await send_prediction_with_chart(application, prices, indicators)

        # 发送消息
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"发送实时行情预测失败: {e}")
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text="抱歉，无法获取实时行情数据，请稍后再试。"
        )

def setup_scheduler(application):
    scheduler = AsyncIOScheduler()
    tz = timezone('Asia/Shanghai')

    # 每小时整点发送预测
    scheduler.add_job(send_hourly_prediction, 'cron', minute=0, args=[application], timezone=tz)

    # 每天10:00发送日报
    scheduler.add_job(send_daily_report_scheduler, 'cron', hour=10, minute=0, args=[application], timezone=tz)

    # 每周日10:00发送周报
    scheduler.add_job(send_weekly_report_scheduler, 'cron', day_of_week='sun', hour=10, minute=0, args=[application], timezone=tz)

    # 每月1日10:00发送月报
    scheduler.add_job(send_monthly_report_scheduler, 'cron', day=1, hour=10, minute=0, args=[application], timezone=tz)

    scheduler.start()

async def send_daily_report_scheduler(application):
    from handlers.messages import send_daily_report
    # 创建一个虚拟的 Update 对象
    class FakeUpdate:
        async def message(self):
            class FakeMessage:
                async def reply_photo(self, photo, caption):
                    pass
            return FakeMessage()
    fake_update = FakeUpdate()
    await send_daily_report(fake_update)

async def send_weekly_report_scheduler(application):
    from handlers.messages import send_weekly_report
    class FakeUpdate:
        async def message(self):
            class FakeMessage:
                async def reply_photo(self, photo, caption):
                    pass
            return FakeMessage()
    fake_update = FakeUpdate()
    await send_weekly_report(fake_update)

async def send_monthly_report_scheduler(application):
    from handlers.messages import send_monthly_report
    class FakeUpdate:
        async def message(self):
            class FakeMessage:
                async def reply_photo(self, photo, caption):
                    pass
            return FakeMessage()
    fake_update = FakeUpdate()
    await send_monthly_report(fake_update)
