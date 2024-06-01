from sklearn.utils.validation import joblib
import torch
from binance import Client
from datetime import datetime
from config import BINANCE_API_KEY, BINANCE_API_SECRET
from data_fetcher import fetch_historical_data
from database import SessionLocal, Trade
from data_preprocessing import preprocess_data
from model import LSTMModel
from rich.console import Console

console = Console()
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def load_model(model_path):
    device = torch.device("cuda")
    model = LSTMModel(input_size=1, hidden_size=50, num_layers=2, output_size=1).to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    return model

def load_scaler(scaler_path):
    return joblib.load(scaler_path)

def predict_price(model, data, scaler):
    device = torch.device("cuda")
    data = torch.from_numpy(data).float().to(device)

    with torch.no_grad():
        prediction = model(data)

    prediction = prediction.cpu().numpy()
    prediction = scaler.inverse_transform(prediction)

    return prediction

def record_trade(symbol, side, price, qty):
    session = SessionLocal()

    total = price * qty

    trade = Trade(
        symbol=symbol,
        side=side,
        price=price,
        qty=qty,
        total=total
    )

    session.add(trade)
    session.commit()
    session.close()

def trading_strategy(model, scaler):
    symbol = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_1HOUR
    klines = client.get_klines(symbol=symbol, interval=interval, limit=1)
    current_price = float(klines[-1][4])

    df = fetch_historical_data(symbol, interval, "1 Jan, 2020", datetime.now().strftime("%d %b, %Y"))
    X, _, _ = preprocess_data(df)

    predirected_price = predict_price(model, X[-1:], scaler)[0][0]

    console.print(f"Currnet price: {current_price}", style="bold green")
    console.print(f"Predicted price: {predirected_price}", style="bold blue")

    side = "BUY" if predirected_price > current_price else "SELL"

    qty = 1

    console.log(f"Side: {side}", style="bold green")

    record_trade(symbol, side, current_price, qty)

    return side, current_price, predirected_price
