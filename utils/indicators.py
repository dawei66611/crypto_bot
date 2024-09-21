# utils/indicators.py

import numpy as np
import talib

def calculate_technical_indicators(prices):
    prices = np.array(prices)
    macd, macd_signal, macd_hist = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    rsi = talib.RSI(prices, timeperiod=14)
    upper, middle, lower = talib.BBANDS(prices, timeperiod=20)
    sma = talib.SMA(prices, timeperiod=30)
    ema = talib.EMA(prices, timeperiod=30)

    return {
        'MACD': macd[-1],
        'MACD_Signal': macd_signal[-1],
        'RSI': rsi[-1],
        'Bollinger_Upper': upper[-1],
        'Bollinger_Middle': middle[-1],
        'Bollinger_Lower': lower[-1],
        'SMA_30': sma[-1],
        'EMA_30': ema[-1]
    }
