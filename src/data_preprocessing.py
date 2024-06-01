import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

def preprocess_data(df):
    scaled_data = scaler.fit_transform(df[["close"]])

    def create_dataset(data, time_step=1):
        X, y = [], []

        for i in range(len(data) - time_step - 1):
            X.append(data[i:(i + time_step), 0])
            y.append(data[i + time_step, 0])

        return np.array(X), np.array(y)

    time_step = 60

    X, y = create_dataset(scaled_data, time_step)
    X = X.reshape(X.shape[0], X.shape[1], 1)

    return X, y, scaler
