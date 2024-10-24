import streamlit as st
from processing import process, preprocess
import numpy as np
import pandas as pd

st.title("Калькулятор глубины и ширины сварного соединения")
# st.header("Пример графика")

# Определяем диапазоны для каждого показателя
RANGES = {
    'IW': {'min': 43.0, 'max': 49.0, 'default': 45.0},
    'IF': {'min': 141.0, 'max': 150.0, 'default': 145.0},
    'VW': {'min': 4.5, 'max': 12.0, 'default': 8.0},
    'FP': {'min': 5.0, 'max': 125.0, 'default': 65.0}
}

# Инициализация состояния для всех переменных
if 'values' not in st.session_state:
    st.session_state['values'] = {
        key: value['default'] for key, value in RANGES.items()
    }


def update_slider(var_name):
    try:
        input_value = float(st.session_state[f'text_{var_name}'])
        if RANGES[var_name]['min'] <= input_value <= RANGES[var_name]['max']:
            st.session_state['values'][var_name] = input_value
    except ValueError:
        pass


def update_text(var_name):
    st.session_state['values'][var_name] = st.session_state[f'slider_{var_name}']


st.title('Ввод показателей')

for var_name in RANGES.keys():
    st.subheader(f'Показатель {var_name}')
    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            f'Введите значение {var_name} ({RANGES[var_name]["min"]}-{RANGES[var_name]["max"]})',
            value=str(st.session_state['values'][var_name]),
            key=f'text_{var_name}',
            on_change=update_slider,
            args=(var_name,)
        )

    with col2:
        st.slider(
            f'Ползунок для {var_name}',
            min_value=RANGES[var_name]['min'],
            max_value=RANGES[var_name]['max'],
            value=float(st.session_state['values'][var_name]),
            key=f'slider_{var_name}',
            on_change=update_text,
            args=(var_name,)
        )

# st.write('Текущие значения показателей:')
# for var_name, value in st.session_state['values'].items():
#     st.write(f'{var_name}: {value}')

# Создаем DataFrame из введенных показателей
data = pd.DataFrame({
    'IW': [st.session_state['values']['IW']],
    'IF': [st.session_state['values']['IF']],
    'VW': [st.session_state['values']['VW']],
    'FP': [st.session_state['values']['FP']]
})

# Выводим DataFrame
st.write('DataFrame из введенных показателей:')
st.dataframe(data)

# Добавляем кнопку для расчета
if st.button('Рассчитать параметры шва'):
    try:
        # Обрабатываем данные
        scaled_data = preprocess(data)
        # считаем показатели
        result = process(scaled_data)

        # Проверяем, что result не None и содержит нужные значения
        if result is not None and len(result) >= 2:
            depth = round(result[0], 3)
            width = round(result[1], 3)
            # Выводим результат
            st.success(f"Глубина шва {depth} и ширина шва {width}")
        else:
            st.error("Не удалось получить результаты расчета")

    except Exception as e:
        st.error(f"Произошла ошибка при расчете: {str(e)}")