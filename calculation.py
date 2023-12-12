import streamlit as st
import json
import pandas as pd
import datetime as dt
from datetime import datetime

from dateutil import relativedelta

st.set_page_config(layout="wide")
st.title("Калькулятор")
st.markdown("### Если за отчетный период был перевод просьба указать, если нет переходи к рассчету премии")
on = st.toggle("Был перевод")

uploaded_file = st.file_uploader(
    "Choose your database", accept_multiple_files=False)
if uploaded_file is not None:
    file_name = uploaded_file
else:
    file_name = "data.xlsx"

@st.cache_data
def load_data():
    
    df_load = pd.read_excel(file_name, sheet_name="P_RD")
    df_load["Срок выдачи (факт)"] = df_load["Срок выдачи (факт)"].apply(pd.to_datetime, format = "%Y-%m-%d")


    df_izm = pd.read_excel(file_name, sheet_name="IZM")
    df_izm["Дата изменения (факт)"] = df_izm["Дата изменения (факт)"].apply(pd.to_datetime, format = "%Y-%m-%d")

    df_productivity = pd.read_excel(file_name, sheet_name="Productivity_group")
    df_productivity["Дата"] = df_productivity["Дата"].apply(pd.to_datetime, format = "%Y-%m-%d")
    
    return df_load, df_izm, df_productivity

df_load,  df_izm, df_productivity = load_data()

st.dataframe(df_load)
