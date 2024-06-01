from train import train_model

def test_train():
    model, scaler = train_model()
    print("Model trained and saved as lstm_model.pth")

if __name__ == "__main__":
    test_train()
