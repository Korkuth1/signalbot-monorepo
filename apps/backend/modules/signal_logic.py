def check_signal(indicators: dict, current_price: float) -> bool:
    rsi = indicators["rsi"]
    macd = indicators["macd_line"]
    signal = indicators["signal_line"]
    vwap = indicators["vwap"]
    ema_50 = indicators["ema_50"]
    ema_200 = indicators["ema_200"]
    bb_lower = indicators["bb_lower"]

    return (
        rsi < 30 and
        macd > signal and
        current_price < vwap and
        ema_50 > ema_200 and 
        current_price <= bb_lower
    )
