import streamlit as st
import numpy as np
import pandas as pd


st.title("Пример приложения с помощью Streamlit")

st.header("Пример графика")

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.markdown("Текст про **карту**")
df = pd.DataFrame(
    np.random.randn(100, 2) / [0.5, 0.5] + [55.5, 37.33],
    columns=['lat', 'lon'])
st.map(df)


agree = st.checkbox('I agree')
if agree:
    st.markdown("Он согласен")
