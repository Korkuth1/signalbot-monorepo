import pandas as pd

def calculate_indicators(df: pd.DataFrame) -> dict:
    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    rsi_series = calculate_rsi(close)
    macd_line, signal_line = calculate_macd(close)
    vwap = calculate_vwap(df)

    ema_50 = close.ewm(span=50, adjust=False).mean()
    ema_200 = close.ewm(span=200, adjust=False).mean()

    upper_bb, lower_bb = calculate_bollinger_bands(close)

    return {
        "rsi": rsi_series.iloc[-1].item(),
        "macd_line": macd_line.iloc[-1].item(),
        "signal_line": signal_line.iloc[-1].item(),
        "high": high.iloc[-1].item(),
        "low": low.iloc[-1].item(),
        "volume": volume.iloc[-1].item(),
        "vwap": vwap.iloc[-1].item(),
        "ema_50": ema_50.iloc[-1].item(),
        "ema_200": ema_200.iloc[-1].item(),
        "bb_upper": upper_bb.iloc[-1].item(),
        "bb_lower": lower_bb.iloc[-1].item(),
    }

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    vwap = (typical_price * df["Volume"]).cumsum() / df["Volume"].cumsum()
    return vwap

def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()

def calculate_bollinger_bands(series: pd.Series, period=20, std_dev=2):
    sma = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper_band = sma + std_dev * std
    lower_band = sma - std_dev * std
    return upper_band, lower_band
