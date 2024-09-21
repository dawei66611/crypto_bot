# utils/market_data.py

import os
import aiohttp
from config import CMC_API_KEY
import logging

logger = logging.getLogger(__name__)

async def fetch_cmc_market_data(symbol='BTC'):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=parameters) as response:
            if response.status != 200:
                logger.error(f"CMC API 请求失败，状态码：{response.status}")
                raise Exception("Failed to fetch CMC data")
            data = await response.json()
            if 'data' in data and symbol in data['data']:
                price = data['data'][symbol]['quote']['USD']['price']
                return price
            else:
                logger.error("CMC API 返回数据格式错误")
                raise Exception("Failed to fetch CMC data")
