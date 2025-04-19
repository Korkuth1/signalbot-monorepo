import time
import yfinance as yf
import pandas as pd
from modules.indicators import calculate_indicators
from modules.signal_logic import check_signal
from modules.notifier import send_email
from modules.symbols import load_symbols_from_file, save_symbols_to_file, get_all_symbols
from dotenv import load_dotenv
import os
from modules.database import (
    init_db,
    save_signal,
    save_symbols_to_database,
    load_symbols_from_database
)

load_dotenv()

init_db()


def normalize_symbol(symbol: str) -> str:
    if symbol.endswith(".DE.DE"):
        return symbol.replace(".DE.DE", ".DE")
    if symbol.endswith(".PA.PA"):
        return symbol.replace(".PA.PA", ".PA")
    if symbol.endswith(".TO.TO"):
        return symbol.replace(".TO.TO", ".TO")
    if symbol.endswith(".L.L"):
        return symbol.replace(".L.L", ".L")
    return symbol


def run_bot():
    symbols = load_symbols_from_database()

    if not symbols:
        print("Lade Symbole von Quellen und speichere in DB ...")
        all_symbols = get_all_symbols()
        save_symbols_to_database(all_symbols)
        symbols = all_symbols

    for raw_symbol in symbols:
        symbol = normalize_symbol(raw_symbol)

        try:
            print(f"Prüfe {symbol} ...")
            df = yf.download(symbol, period="3mo", interval="1d", progress=False)
            if df.empty or len(df) < 26:
                print(f"Unzureichende Daten für {symbol}")
                continue

            indicators = calculate_indicators(df)

            print(
                f"{symbol}: RSI={indicators['rsi']:.2f}, "
                f"MACD={indicators['macd_line']:.4f}, "
                f"Signal={indicators['signal_line']:.4f}, "
                f"High={indicators['high']:.2f}, "
                f"Low={indicators['low']:.2f}, "
                f"Vol={indicators['volume']:.0f}, "
                f"VWAP={indicators['vwap']:.2f}, "
                f"EMA50={indicators['ema_50']:.2f}, EMA200={indicators['ema_200']:.2f}, "
                f"BB[U/L]={indicators['bb_upper']:.2f}/{indicators['bb_lower']:.2f}"
            )

            current_price = df["Close"].iloc[-1]
            print(f"{symbol}: Signal check = {check_signal(indicators, current_price)}")
            if check_signal(indicators, current_price):
                print(f"Kaufsignal für {symbol} erkannt!")
                send_email(
                    f"Kaufsignal für {symbol}",
                    f"RSI: {indicators['rsi']:.2f}, MACD: {indicators['macd_line']:.4f}, Signal: {indicators['signal_line']:.4f}"
                )

                save_signal(symbol, "buy", indicators)

            time.sleep(1.5)

        except Exception as e:
            print(f"Fehler bei {symbol}: {e}")
            continue


if __name__ == "__main__":
    print("SignalBot läuft ... (alle 5 Minuten)")
    while True:
        run_bot()
        time.sleep(300)
