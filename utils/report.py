import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_daily_report():
    # 示例数据
    data = {
        "时间段": ["10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00"],
        "预测方向": ["上涨", "下跌", "上涨", "下跌"],
        "对错": ["✔", "✖", "✔", "✖"],
        "盈亏金额": ["+200USDT", "-100USDT", "+150USDT", "-50USDT"]
    }
    df = pd.DataFrame(data)
    return df

def generate_weekly_report():
    # 示例数据
    data = {
        "日期": ["9/16", "9/17", "9/18", "9/19", "9/20"],
        "盈亏": ["+200USDT", "-150USDT", "+300USDT", "-100USDT", "+50USDT"]
    }
    df = pd.DataFrame(data)
    return df

def generate_monthly_report():
    # 示例数据
    data = {
        "日期": ["9/01", "9/02", "9/03", "9/04", "9/05"],
        "盈亏": ["+500USDT", "-100USDT", "+150USDT", "-50USDT", "+200USDT"]
    }
    df = pd.DataFrame(data)
    return df

def plot_report(df, title):
    plt.figure(figsize=(8, 6))
    plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    plt.axis('off')
    plt.title(title)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

