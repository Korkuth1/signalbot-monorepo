import pandas as pd
import re
from yahooquery import Screener

def find_ticker_column(tables):
    for idx, table in enumerate(tables):
        print(f"\n Tabelle {idx} Spalten: {table.columns.tolist()}")
        for col in table.columns:
            if re.search(r"symbol|ticker", str(col), re.IGNORECASE):
                print(f"Ticker gefunden in Tabelle {idx}, Spalte: {col}")
                return table[col].dropna().tolist()
    raise ValueError("Keine gültige Ticker-Spalte gefunden.")

def get_sp500_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_dax_symbols():
    url = "https://en.wikipedia.org/wiki/DAX"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_mdax_symbols():
    url = "https://en.wikipedia.org/wiki/MDAX"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_ftse_symbols():
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_cac40_symbols():
    url = "https://en.wikipedia.org/wiki/CAC_40"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_russell1000_symbols():
    url = "https://en.wikipedia.org/wiki/Russell_1000_Index"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_nasdaq100_symbols():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_stoxx50_symbols():
    url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_tsx60_symbols():
    url = "https://en.wikipedia.org/wiki/S%26P/TSX_60"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_asx200_symbols():
    url = "https://en.wikipedia.org/wiki/S%26P/ASX_200"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_russell2000_symbols():
    url = "https://en.wikipedia.org/wiki/Russell_2000_Index"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_symbols_from_yahoo_screen(screen_id, count=1000):
    s = Screener()
    all_symbols = []
    offset = 0

    while True:
        data = s.get_screeners(screen_id, count=count, offset=offset)
        quotes = data.get(screen_id, {}).get('quotes', [])
        if not quotes:
            break
        symbols = [q['symbol'] for q in quotes if 'symbol' in q]
        all_symbols.extend(symbols)
        offset += count

    return list(set(all_symbols))

def get_us_screener_symbols():
    categories = [
        "day_gainers",
        "day_losers",
        "most_actives",
        "undervalued_large_caps",
        "growth_technology_stocks"
    ]
    all_symbols = []

    for cat in categories:
        try:
            symbols = get_symbols_from_yahoo_screen(cat)
            print(f"{len(symbols)} Symbole aus '{cat}': {symbols}")
            all_symbols.extend(symbols)
        except Exception as e:
            print(f"Fehler beim Yahoo-Screener {cat}: {e}")

    result = list(set(all_symbols))
    print(f"\n Insgesamt {len(result)} eindeutige Symbole aus allen Yahoo-Screenern.")
    return result

def get_us_large_caps():
    s = Screener()
    data = s.get_screeners('day_gainers')  # Alternativen: 'most_actives', 'day_losers'
    quotes = data.get('day_gainers', {}).get('quotes', [])
    return [q['symbol'] for q in quotes if 'symbol' in q]

def get_ftse100_symbols():
    import pandas as pd

    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def get_euro_stoxx_50_symbols():
    import pandas as pd

    url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
    tables = pd.read_html(url)
    return find_ticker_column(tables)

def find_ticker_column(tables):
    for i, table in enumerate(tables):
        for col in table.columns:
            col_str = str(col).lower()
            if "symbol" in col_str or "ticker" in col_str:
                print(f"\n✅ Ticker gefunden in Tabelle {i}, Spalte: {col}")
                return table[col].dropna().astype(str).tolist()
        print(f"\n📄 Tabelle {i} Spalten: {list(table.columns)}")
    raise ValueError("❌ Keine gültige Ticker-Spalte gefunden.")

def get_all_symbols():
    sources = [
        ("S&P 500", get_sp500_symbols, lambda s: s),
        ("DAX", get_dax_symbols, lambda s: s + ".DE"),
        ("MDAX", get_mdax_symbols, lambda s: s + ".DE"),
        ("CAC 40", get_cac40_symbols, lambda s: s + ".PA"),
        ("FTSE 100", get_ftse100_symbols, lambda s: s + ".L"),
        ("EURO STOXX 50", get_euro_stoxx_50_symbols, lambda s: s + ".STOXX"),
        ("TSX 60", get_tsx60_symbols, lambda s: s + ".TO"),
        ("ASX 200", get_asx200_symbols, lambda s: s + ".AX"),
    ]

    all_symbols = []

    for name, fetch_func, formatter in sources:
        try:
            print(f"🔍 Lade {name} Symbole ...")
            raw_symbols = fetch_func()
            formatted = [formatter(s) for s in raw_symbols if s]
            all_symbols.extend(formatted)
            print(f"✅ {len(formatted)} Symbole von {name} hinzugefügt.")
        except Exception as e:
            print(f"❌ Fehler bei {name}: {e}")

    print(f"📦 Insgesamt {len(all_symbols)} Symbole gesammelt.\n")
    return list(set(all_symbols))


def save_symbols_to_file(path="symbols.csv"):
    symbols = get_all_symbols()
    pd.Series(symbols).to_csv(path, index=False)
    print(f"{len(symbols)} Symbole gespeichert in {path}")

def load_symbols_from_file(path="symbols.csv"):
    try:
        return pd.read_csv(path).iloc[:, 0].dropna().tolist()
    except Exception as e:
        print(f"Fehler beim Laden der Symbole: {e}")
        return []
