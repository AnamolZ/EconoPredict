from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import os
from priceScrappy import StockPrice

class LoadingModel(StockPrice):
    def __init__(self, stock_symbol, input_data_path, trained_model):
        super().__init__(stock_symbol)

        self.stock_symbol = stock_symbol
        self.input_data_path = input_data_path
        self.trained_model = trained_model
        self.model = load_model(self.trained_model)

        self.predicted_price = None
        self.initial_price = float(self.scrape_price())

        self.process_data()
        # Update predicted price
        self.predicted_price = self.predicting_value()
    
    def predicting_value(self):
        input_data_frame = pd.read_csv(self.input_data_path, index_col=0)
        input_data_frame['date'] = pd.to_datetime(input_data_frame.index)

        scaler = MinMaxScaler((0, 1))
        scaled_data = scaler.fit_transform(input_data_frame['Close'].values.reshape(-1, 1))

        data_reshape = np.reshape(scaled_data[-15:], (1, 1, 15))
        prediction = self.model.predict(data_reshape)
        self.predicted_price = scaler.inverse_transform(prediction)[0, 0]

        return self.predicted_price

    def percentage_change(self):
        percentage_change = ((self.predicted_price - self.initial_price) / self.initial_price) * 100

        if percentage_change > 0:
            return f'↟Up {percentage_change:.2f}%'
        elif percentage_change < 0:
            return f'↯Down {abs(percentage_change):.2f}%'
        else:
            return "No significant change"

        if os.path.exists(self.input_data_path):
            os.remove(self.input_data_path)

# For Manual Testing
if __name__ == "__main__":
    LoadingModel = LoadingModel("AMZN","TrainingData.csv","LSTMmodel.h5")
    print(LoadingModel.percentage_change())
