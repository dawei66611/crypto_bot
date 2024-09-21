# utils/gpt_analysis.py

import openai
from config import OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

openai.api_key = OPENAI_API_KEY

async def generate_gpt_analysis(indicators, news_analysis):
    prompt = f"""
    请根据以下技术指标和新闻分析，为BTC的下一小时价格趋势提供详细的分析报告。

    技术指标：
    MACD: {indicators['MACD']}
    MACD 信号线: {indicators['MACD_Signal']}
    RSI: {indicators['RSI']}
    Bollinger Bands 上轨: {indicators['Bollinger_Upper']}
    Bollinger Bands 中轨: {indicators['Bollinger_Middle']}
    Bollinger Bands 下轨: {indicators['Bollinger_Lower']}

    新闻分析：
    {news_analysis}

    请总结分析并预测BTC下一小时的价格趋势，并说明原因。
    """

    try:
        response = await openai.Completion.acreate(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            n=1,
            stop=None
        )
        analysis = response.choices[0].text.strip()
        return analysis
    except Exception as e:
        logger.error(f"GPT 生成分析报告失败: {e}")
        return "无法生成详细的分析报告。"

