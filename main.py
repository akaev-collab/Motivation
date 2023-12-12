import pandas as pd
import streamlit as st
import json
import altair as alt

st.set_page_config(layout="wide")
st.title("Дашборд")

def load_data():
    
    file_name = "data.xlsx"
    df_load_group = pd.read_excel(file_name, sheet_name="P_RD_group")

    df_izm_group = pd.read_excel(file_name, sheet_name="IZM_group")

    df_productivity_group = pd.read_excel(file_name, sheet_name="Productivity_group")

    return df_load_group, df_izm_group, df_productivity_group

df_load_group, df_izm_group, df_productivity_group = load_data()

path_to_json = "Structure/structure.json"

with open (path_to_json, "r", encoding='utf-8') as file:
    structure = json.load(file)

d = []
master_merge_dict = {}
for i in structure.keys():
    d.append(structure[i])

for i in d:
    for key, value in i.items():
        master_merge_dict[key] = value
        
filter_selected_master = st.multiselect("Мастерская", master_merge_dict.keys(), master_merge_dict.keys())
tabel_1, tabel_2, tabel_3 = st.tabs(["Готовность", "Качество", "Выработка"])

with tabel_1:
   st.header("Готовность")
    
with tabel_2:
   st.header("Качество")
   
with tabel_3:
   st.header("Выработка")

st.dataframe(df_izm_group)
