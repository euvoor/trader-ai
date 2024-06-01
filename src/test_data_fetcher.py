from binance import Client
from data_fetcher import fetch_historical_data

def test_data_fetcher():
    df = fetch_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Jan, 2020", "1 Jan, 2022")
    print(df.head())

if __name__ == "__main__":
    test_data_fetcher()
