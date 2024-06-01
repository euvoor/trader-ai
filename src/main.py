from database import create_tables
from trade import load_model, load_scaler, trading_strategy
from train import train_model
import argparse

if __name__ == "__main__":
    # create_tables()

    parser = argparse.ArgumentParser(description="AI Trading Bot")
    parser.add_argument("--train", action="store_true", help="Train the model")
    parser.add_argument("--trade", action="store_true", help="Run trading strategy")

    args = parser.parse_args()

    if args.train:
        model, scaler = train_model()

    if args.trade:
        model = load_model("lstm_model.pth")
        scaler = load_scaler("scaler.pkl")

        trading_strategy(model, scaler)
