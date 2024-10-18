import pandas as pd
# import numpy as np
import joblib


# import pickle


def preprocess(data):
    try:
        min_max_scaler_x = joblib.load('./models/min_max_scaler_x.joblib')
        print("Scaler_x loaded successfully.")
    except FileNotFoundError:
        print("Error: Joblib file_x not found.")
        return None
    except Exception as e:
        print(f"An error_x occurred: {e}")
        return None

    scaled_data = min_max_scaler_x.transform(data)
    return scaled_data


def process(scaled_data):
    try:
        min_max_scaler_y = joblib.load('./models/min_max_scaler_y.joblib')
        print("Scaler_y loaded successfully.")
    except FileNotFoundError:
        print("Error: Joblib file_y not found.")
        return None
    except Exception as e:
        print(f"An error_y occurred: {e}")
        return None

    # Преобразуем словарь в DataFrame
    data_df = pd.DataFrame(scaled_data)

    # Загружаем обученную модель
    loaded_model = joblib.load('models/DT_model.joblib')

    # Предсказываем параметры шва
    scaled_y = loaded_model.predict(data_df)

    depth, width = min_max_scaler_y.inverse_transform([scaled_y])

    # Убираем квадратные скобки
    # price = price[0, 0]


    return depth, width
