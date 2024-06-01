import joblib
import torch
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from model import LSTMModel
from data_preprocessing import preprocess_data
from data_fetcher import fetch_historical_data
from rich.console import Console
from binance import Client

console = Console()

def train_model():
    console.print("Fetching data...", style="bold green")
    df = fetch_historical_data("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 Jan, 2020", "1 Jan, 2022")
    X, y, scaler = preprocess_data(df)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LSTMModel(input_size=1, hidden_size=50, num_layers=2, output_size=1).to(device)
    criterion = torch.nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    X_train = torch.from_numpy(X).float().to(device)
    y_train = torch.from_numpy(y).float().to(device)

    dataset = TensorDataset(X_train, y_train)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

    num_epochs = 100
    for epoch in range(num_epochs):
        model.train()
        for X_batch, y_batch in dataloader:
            outputs = model(X_batch).view(-1)  # Reshape outputs to [batch_size]
            y_batch = y_batch.view(-1)         # Reshape y_batch to [batch_size]
            optimizer.zero_grad()
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 10 == 0:
            console.print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}', style="bold blue")

    console.print("Training complete!", style="bold green")
    torch.save(model.state_dict(), "lstm_model.pth")

    joblib.dump(scaler, "scaler.pkl")

    return model, scaler
