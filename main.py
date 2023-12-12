import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.title("Дашборд")

def load_data():
    
    file_name = "data.xlsx"
    df_load_group = pd.read_excel(file_name, sheet_name="P_RD_group")
    df_izm_group = pd.read_excel(file_name, sheet_name="IZM_group")
    df_productivity_group = pd.read_excel(file_name, sheet_name="Productivity_group")
    
    return df_load_group, df_izm_group, df_izm_group

df_load_group, df_izm_group, df_izm_group = load_data()

path_to_json = "Structure"

with open (path_to_json +"/structure.json", "r", encoding='utf-8') as file:
    structure = json.load(file) # зависимость мастерской и группу от управления

d = []
master_merge_dict = {}
for i in structure.keys():
    d.append(structure[i])

for i in d:
    for key, value in i.items():
        master_merge_dict[key] = value
        

selected = option_menu(None, options=["Готовность", "Качество", "Выработка","Инициативы"],
                            icons=['bar-chart-steps','bricks','hexagon-half','diagram-2'],
                            orientation="horizontal")

filter_selected_master = st.multiselect("Мастерская", master_merge_dict.keys(), master_merge_dict.keys())

st.dataframe(df_load_group)
