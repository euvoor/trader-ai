from binance import Client
from data_fetcher import fetch_historical_data
from data_preprocessing import preprocess_data

def test_data_preprocessing():
    df = fetch_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Jan, 2020", "1 Jan, 2022")
    X, y, scaler = preprocess_data(df)

    #  print("X shape: ", X.shape)
    #  print("y shape: ", y.shape)
    #  print("First X sample: ", X[0])
    #  print("First y sample: ", y[0])

if __name__ == "__main__":
    test_data_preprocessing()
