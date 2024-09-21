# utils/news.py

import os
import aiohttp
from config import NEWS_API_KEY
import logging

logger = logging.getLogger(__name__)

async def fetch_latest_news(keyword='Bitcoin'):
    url = 'https://newsapi.org/v2/everything'
    parameters = {
        'q': keyword,
        'apiKey': NEWS_API_KEY,
        'language': 'zh',
        'sortBy': 'publishedAt',
        'pageSize': 5
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=parameters) as response:
            if response.status != 200:
                logger.error(f"News API 请求失败，状态码：{response.status}")
                raise Exception("Failed to fetch news data")
            data = await response.json()
            if data['status'] == 'ok':
                articles = data['articles']
                news_list = [article['title'] for article in articles]
                return news_list
            else:
                logger.error("News API 返回数据格式错误")
                raise Exception("Failed to fetch news data")

