from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import os
from dataRetriever import func

def PulseAI(req):
    loaded_model = load_model("LSTMmodel.h5")

    initial_price = func(req)
    TrainningData = "TrainningData.csv" 
    new_data_df = pd.read_csv("TrainningData.csv", index_col=0)
    new_data_df['date'] = pd.to_datetime(new_data_df.index)

    min_max_scaler = MinMaxScaler(feature_range=(0, 1))
    min_max_scaler.fit_transform(new_data_df['Close'].values.reshape(-1, 1))

    new_dataset = min_max_scaler.transform(new_data_df['Close'].values.reshape(-1, 1))
    x_new = np.reshape(new_dataset[-15:], (1, 1, 15))

    new_predictions = loaded_model.predict(x_new)
    new_predictions = min_max_scaler.inverse_transform(new_predictions)

    last_date = new_data_df['date'].iloc[-1]
    next_day_date = last_date + pd.DateOffset(days=1)
    final_price = new_predictions[0, 0]
    percentage_change = ((final_price - initial_price) / initial_price) * 100

    if percentage_change < 0:
        return (f'Price {new_predictions[0, 0]:.2f} ↟Up {abs(percentage_change):.2f}%')

    elif percentage_change > 0:
        return (f'Price {new_predictions[0, 0]:.2f} ↯Down {abs(percentage_change):.2f}%')
    else:
        print("NDU")
        pass

    os.remove(TrainningData) if os.path.exists(TrainningData) else None