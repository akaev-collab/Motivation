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

chart_width = 1200
chart_height = 400

tabel_1, tabel_2, tabel_3 = st.tabs(["Готовность", "Качество", "Выработка"])

with tabel_1:
    st.header("Готовность")
    df_load_group = df_load_group[df_load_group["Мастерская"].isin(filter_selected_master)]
    df_load_plan = df_load_group.groupby([df_load_group["Дата"].dt.strftime("%Y-%m-1")]).aggregate({"План":"sum"}).reset_index()
    df_load_fact = df_load_group.groupby([df_load_group["Дата"].dt.strftime("%Y-%m-1")]).aggregate({"Факт":"sum"}).reset_index()

    bar_load_plan = alt.Chart(df_load_plan).mark_bar(width=22, xOffset=-10, color="grey").encode(
        alt.X("Дата:T", title="", axis=alt.Axis(format="%m.%Y")),
        y = "План", 
        tooltip=["Дата:T", "План"]
    ).properties(width=chart_width, height=chart_height)

    bar_load_fact = alt.Chart(df_load_fact, title = "Динамика выдачи комплектов").mark_bar(width=22, xOffset=10, color = "#007FFF").encode(
        alt.X("Дата:T"),
        y = "Факт",
        tooltip=["Дата:T", "Факт"]
    ).properties(width=chart_width, height=chart_height)

    df_load_fact_total = df_load_group.groupby(["Мастерская", "Статус по выдаче"], as_index=False).aggregate({"Факт":"sum"})

    bar_load_fact_total = alt.Chart(df_load_fact_total, title = "Статус по выданым комплектам").mark_bar().encode(
        alt.X("Факт", title=""),
        alt.Y("Мастерская", title=""),
        color = "Статус по выдаче"
    ).properties(width=chart_width, height=chart_height)
    st.altair_chart(bar_load_plan + bar_load_fact)
    st.altair_chart(bar_load_fact_total)
    
with tabel_2:
    st.header("Качество")
   
with tabel_3:
   st.header("Выработка")

st.dataframe(df_izm_group)
