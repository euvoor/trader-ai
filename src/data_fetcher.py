from binance import Client
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from config import BINANCE_API_KEY, BINANCE_API_SECRET
import pandas as pd
from database import engine, HistoricalDataCache
import json
from datetime import datetime

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
Session = sessionmaker(bind=engine)

def fetch_historical_data(symbol, interval, start, end):
    session = Session()

    existing_data = session.query(HistoricalDataCache).filter(
        and_(
            HistoricalDataCache.symbol == symbol,
            HistoricalDataCache.interval == interval,
            HistoricalDataCache.start == start,
            HistoricalDataCache.end == end,
        )
    ).first()

    if existing_data:
        data = json.loads(existing_data.json_data)
    else:
        klines = client.get_historical_klines(symbol, interval, start, end)
        data = klines

        cache_entry = HistoricalDataCache(
            symbol=symbol,
            interval=interval,
            start=start,
            end=end,
            json_data=json.dumps(data)
        )

        session.add(cache_entry)
        session.commit()

    session.close()

    df = pd.DataFrame(data)

    df.columns = [
        "timestamp", "open", "high", "low", "close", "volume", "close_time",
        "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume", "ignore"
    ]

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df[["open", "high", "low", "close", "volume"]]
    df = df.astype(float)

    return df
