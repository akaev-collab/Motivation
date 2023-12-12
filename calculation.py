import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.title("Калькулятор")
st.markdown("### Если за отчетный период был перевод просьба указать, если нет переходи к рассчету премии")
on = st.toggle("Был перевод")

d = pd.read_excel('data.xlsx')

st.dataframe(d)
