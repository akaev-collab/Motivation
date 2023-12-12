import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Калькулятор")
st.markdown("### Если за отчетный период был перевод просьба указать, если нет переходи к рассчету премии")
on = st.toggle("Был перевод")


data = pd.read_excel('data.xlsx', sheet_name="P_RD")

st.dataframe(data)
