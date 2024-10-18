import pandas as pd
import joblib


def preprocess(data):
    try:
        min_max_scaler_x = joblib.load('./models/min_max_scaler_x.joblib')
    except FileNotFoundError:
        print("Error: Joblib file min_max_scaler_x.joblib not found.")
        return None
    except Exception as e:
        print(f"An error_x occurred: {e}")
        return None
    scaled_data = min_max_scaler_x.transform(data)
    return scaled_data


def process(scaled_data):
    try:
        min_max_scaler_y = joblib.load('./models/min_max_scaler_y.joblib')
    except FileNotFoundError:
        print("Error: Joblib file min_max_scaler_y.joblib not found.")
        return None
    except Exception as e:
        print(f"An error_y occurred: {e}")
        return None

    # Загружаем обученную модель
    try:
        loaded_model = joblib.load('./models/DT_model.joblib')
    except FileNotFoundError:
        print("Error: Joblib file DT_model.joblib not found.")
        return None
    except Exception as e:
        print(f"An error_y occurred: {e}")
        return None


    data_df = pd.DataFrame(scaled_data)
    # Предсказываем стоимость
    scaled_y = loaded_model.predict(data_df)
    # Убираем квадратные скобки squeeze()
    result = min_max_scaler_y.inverse_transform(scaled_y).squeeze()

    return result