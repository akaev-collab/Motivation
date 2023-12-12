import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.title("Дашборд")

def load_data():
    
    file_name = "data.xlsx"
    df_load_group = pd.read_excel(file_name, sheet_name="P_RD_group")

    return df_load_group

df_load_group = load_data()

st.dataframe(df_load_group)
