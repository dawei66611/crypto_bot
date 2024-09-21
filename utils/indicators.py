import numpy as np
import talib

def calculate_technical_indicators(prices):
    prices = np.array(prices)
    macd, macd_signal, macd_hist = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    rsi = talib.RSI(prices, timeperiod=14)

    return {
        'MACD': macd[-1],
        'MACD_Signal': macd_signal[-1],
        'RSI': rsi[-1]
    }

