from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # <--- ALLOW ALL ORIGINS FOR /api/*

@app.route('/api/signals', methods=['GET'])
def get_signals():
    conn = sqlite3.connect('signalbot.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            symbol, recommendation, rsi, macd, signal_line, 
            vwap, ema50, ema200, high, low, volume, 
            bb_upper, bb_lower, timestamp 
        FROM signals ORDER BY timestamp DESC
    """)
    signals = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "symbol": s[0],
            "recommendation": s[1],
            "rsi": s[2],
            "macd": s[3],
            "signal_line": s[4],
            "vwap": s[5],
            "ema50": s[6],
            "ema200": s[7],
            "high": s[8],
            "low": s[9],
            "volume": s[10],
            "bb_upper": s[11],
            "bb_lower": s[12],
            "timestamp": s[13]
        } for s in signals
    ])


@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    conn = sqlite3.connect('signalbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT symbol FROM signals ORDER BY symbol ASC")
    symbols = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(symbols)

@app.route('/api/signals/<symbol>', methods=['GET'])
def get_signals_by_symbol(symbol):
    conn = sqlite3.connect('signalbot.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT symbol, recommendation, rsi, macd, signal_line, timestamp FROM signals WHERE symbol = ? ORDER BY timestamp DESC",
        (symbol.upper(),)
    )
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
        {
            "symbol": r[0],
            "recommendation": r[1],
            "rsi": r[2],
            "macd": r[3],
            "signal_line": r[4],
            "timestamp": r[5]
        } for r in rows
    ])

@app.route('/api/signals/latest', methods=['GET'])
def get_latest_signals():
    conn = sqlite3.connect('signalbot.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT symbol, recommendation, rsi, macd, signal_line, timestamp FROM signals ORDER BY timestamp DESC LIMIT 20"
    )
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
        {
            "symbol": r[0],
            "recommendation": r[1],
            "rsi": r[2],
            "macd": r[3],
            "signal_line": r[4],
            "timestamp": r[5]
        } for r in rows
    ])

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(debug=True)
