import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression
from keras.models import Sequential
from keras.layers import LSTM, Dense

data_df = pd.read_csv("TSLA.csv", index_col=0)
data_df['date'] = pd.to_datetime(data_df.index)

scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(data_df['Close'].values.reshape(-1, 1))

train_size = int(len(dataset) * 0.7)
train, test = dataset[:train_size, :], dataset[train_size:, :]

def create_dataset(dataset, look_back=15):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        dataX.append(dataset[i:(i+look_back), 0])
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

look_back = 15
x_train, y_train = create_dataset(train, look_back)
x_test, y_test = create_dataset(test, look_back)

x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

estimator = LogisticRegression()
model = SequentialFeatureSelector(estimator)

model = Sequential()
model.add(LSTM(20, input_shape=(1, look_back)))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=20, batch_size=1, verbose=2)
model.save("LSTMmodel", save_format="tf")
