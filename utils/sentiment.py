# utils/sentiment.py

def analyze_market_sentiment(news_list):
    sentiment_score = 0
    for news in news_list:
        if any(keyword in news for keyword in ["利好", "上涨", "增长", "突破"]):
            sentiment_score += 1
        elif any(keyword in news for keyword in ["利空", "下跌", "下降", "回落"]):
            sentiment_score -= 1

    if sentiment_score > 2:
        return "积极"
    elif sentiment_score < -2:
        return "消极"
    else:
        return "中性"

