from sqlalchemy import (
    create_engine, Column, String, Float, Integer, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import sqlite3

Base = declarative_base()
engine = create_engine("sqlite:///signalbot.db")
Session = sessionmaker(bind=engine)


# Tabelle für Signale
class Signal(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String)
    recommendation = Column(String)
    rsi = Column(Float)
    macd = Column(Float)
    signal_line = Column(Float)
    vwap = Column(Float)
    ema50 = Column(Float)
    ema200 = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    bb_upper = Column(Float)
    bb_lower = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


# Tabelle für verfügbare Symbole
class Symbol(Base):
    __tablename__ = "symbols"

    name = Column(String, primary_key=True)


# Initialisiere Tabellen
def init_db():
    Base.metadata.create_all(engine)


def safe(val):
    return val if val is not None else 0.0


def save_signal(symbol, recommendation, indicators):
    session = Session()
    try:
        signal = Signal(
            symbol=symbol,
            recommendation=recommendation,
            rsi=safe(indicators.get('rsi')),
            macd=safe(indicators.get('macd_line')),
            signal_line=safe(indicators.get('signal_line')),
            vwap=safe(indicators.get('vwap')),
            ema50=safe(indicators.get('ema_50')),
            ema200=safe(indicators.get('ema_200')),
            high=safe(indicators.get('high')),
            low=safe(indicators.get('low')),
            volume=int(indicators.get('volume') or 0),
            bb_upper=safe(indicators.get('bb_upper')),
            bb_lower=safe(indicators.get('bb_lower')),
            timestamp=datetime.utcnow()
        )
        session.add(signal)
        session.commit()
    except IntegrityError as e:
        print(f"Fehler beim Speichern: {e}")
        session.rollback()
    finally:
        session.close()


def save_symbols_to_database(symbols: list[str]):
    session = Session()
    existing = {s.name for s in session.query(Symbol).all()}
    new = [Symbol(name=s) for s in symbols if s not in existing]

    if new:
        session.add_all(new)
        session.commit()
        print(f"{len(new)} neue Symbole in der DB gespeichert.")
    else:
        print("ℹ Keine neuen Symbole.")

    session.close()


def load_symbols_from_database() -> list[str]:
    session = Session()
    symbols = [s.name for s in session.query(Symbol).all()]
    session.close()
    return symbols
