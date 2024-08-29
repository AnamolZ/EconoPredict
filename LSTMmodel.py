import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class ModelCreation:
    def __init__(self, training_data_path: str, look_back: int = 15):
        self.training_data_path = training_data_path
        self.look_back = look_back
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.train_data = None
        self.test_data = None
        self.model = None

    def data_frame_training(self):
        training_data_frame = pd.read_csv(self.training_data_path, index_col=0)
        training_data_frame['date'] = pd.to_datetime(training_data_frame.index)        

        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(training_data_frame['Close'].values.reshape(-1,1))

        train_size = int(len(scaled_data) * 0.7)
        self.train_data, self.test_data = scaled_data[:train_size], scaled_data[train_size:]

    def generate_sequences(self, dataset, look_back=15):
        X, y = [], []
        for i in range(len(dataset) - look_back):
            X.append(dataset[i:i + look_back])
            y.append(dataset[i + look_back])
        return np.array(X), np.array(y)

    def train(self):
        if self.train_data is None or self.test_data is None:
            raise RuntimeError("Data has not been prepared. Call 'data_frame_training' first.")

        x_train, y_train = self.generate_sequences(self.train_data, self.look_back)
        x_test, y_test = self.generate_sequences(self.test_data, self.look_back)

        x_train = np.reshape(x_train, (x_train.shape[0], self.look_back, 1))
        x_test = np.reshape(x_test, (x_test.shape[0], self.look_back, 1))

        self.model = Sequential([
            LSTM(20, input_shape=(self.look_back, 1)),
            Dense(1)
        ])

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(x_train, y_train, epochs=20, batch_size=1, verbose=2)
        self.model.save("LSTMmodel.h5")

# For Manual Testing
if __name__ == "__main__":
    model = ModelCreation(training_data_path="TrainingData.csv")
    model.data_frame_training()
    model.train()