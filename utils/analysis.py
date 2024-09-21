def generate_prediction_analysis(prices, indicators):
    # 简单的预测分析示例
    macd = indicators.get('MACD', 0)
    rsi = indicators.get('RSI', 0)

    if macd > 0 and rsi < 70:
        return "根据MACD和RSI指标，BTC短期内有上涨趋势。"
    elif macd < 0 and rsi > 30:
        return "根据MACD和RSI指标，BTC短期内可能下跌。"
    else:
        return "BTC短期内趋势不明，建议观望。"

def generate_news_analysis(news):
    # 示例新闻分析
    if "利好" in news or "上涨" in news:
        return "新闻显示市场有利好消息，可能推动BTC价格上涨。"
    elif "利空" in news or "下跌" in news:
        return "新闻显示市场有利空消息，可能导致BTC价格下跌。"
    else:
        return "新闻没有明显利好或利空，市场可能保持震荡。"

