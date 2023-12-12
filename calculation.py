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


@st.cache_data
def load_data():
    
    path_to_data = r"C:\Users\User\Documents\Google Диск\Samolet\Motivation\DPI\DataFrame\DataFrame.xlsx"
    df_load = pd.read_excel(path_to_data, sheet_name="P_RD")
    df_load["Срок выдачи (факт)"] = df_load["Срок выдачи (факт)"].apply(pd.to_datetime, format = "%Y-%m-%d")


    df_izm = pd.read_excel(path_to_data, sheet_name="IZM")
    df_izm["Дата изменения (факт)"] = df_izm["Дата изменения (факт)"].apply(pd.to_datetime, format = "%Y-%m-%d")

    df_productivity = pd.read_excel(path_to_data, sheet_name="Productivity_group")
    df_productivity["Дата"] = df_productivity["Дата"].apply(pd.to_datetime, format = "%Y-%m-%d")
    
    return df_load, df_izm, df_productivity

df_load,  df_izm, df_productivity = load_data()


path_to_json = r"C:\Users\User\Documents\Google Диск\Samolet\Motivation\DPI\Dashboard\Structure_JSON"

with open (path_to_json +"\greid_level.json", "r", encoding='utf-8') as file: 
    greid_level = json.load(file) # зависимость процента премии от грейда

with open (path_to_json +"\position.json", "r", encoding='utf-8') as file:
    position = json.load(file) # завимимости должности от управления

with open (path_to_json +"\structure.json", "r", encoding='utf-8') as file:
    structure = json.load(file) # зависимость мастерской и группу от управления

# Статус выдаче комплетов
def load_status(data_frame):
    
    load_df = data_frame[(data_frame["Мастерская"] == master_select) & (data_frame["Группа"] == master_group) & \
                   ((data_frame["Срок выдачи (факт)"] >= pd.to_datetime(str(start_period))) & (data_frame["Срок выдачи (факт)"] <= pd.to_datetime(str(end_period))))]
    
    load_df = load_df.groupby("Статус по выдаче", as_index = False).aggregate({"Кол-во комплектов (факт)":"sum"})
    
    time_load      = load_df[load_df["Статус по выдаче"] == "в срок"]["Кол-во комплектов (факт)"].sum()
    time_less_load = load_df[load_df["Статус по выдаче"] == "с задержкой (<14 дней)"]["Кол-во комплектов (факт)"].sum()
    time_more_load = load_df[load_df["Статус по выдаче"] == "с задержкой (>14 дней)"]["Кол-во комплектов (факт)"].sum()
    
    percent_load = (time_load / (load_df["Кол-во комплектов (факт)"].sum()))
    

    if len(load_df) == 0:
        percent_load = 0
    else:
        if time_more_load != 0 or percent_load < 0.8:
            prize_to_load = 0
        elif percent_load >= 0.8 and percent_load < 1:
            prize_to_load = percent_load
        elif percent_load == 1:
            prize_to_load = 0.35

    return load_df, prize_to_load

# Качество документации

def izm_status(data_frame):
    df_izm = data_frame[(data_frame["Мастерская"] == master_select) & (data_frame["Группа\Виновник"] == master_group) &\
                ((data_frame["Дата изменения (факт)"] >= pd.to_datetime(str(start_period))) & (data_frame["Дата изменения (факт)"] <= pd.to_datetime(str(end_period))))]
    if len(df_izm) != 0:
        df_izm = df_izm.groupby(["Мастерская", "Группа\Виновник"], as_index = False).aggregate({"Общее кол-во листов по разделам ":"sum", "Кол-во листов по разделам":"sum"})

        df_izm["% ИЗМ"] =  (df_izm["Кол-во листов по разделам"] / df_izm["Общее кол-во листов по разделам "])*100


        if len(df_izm) == 0:
            percent_izm = 0
        else:
            percent_izm = df_izm["% ИЗМ"].sum()
            if percent_izm == 0:
                prize_to_izm = 1.2
            elif percent_izm > 0 and percent_izm <= 3:
                prize_to_izm = 1
            else: 
                prize_to_izm = 0
    else:
        prize_to_izm = 0
    
    return prize_to_izm

# Выработка

def productivity_status(data_frame):
    df_productivity = data_frame[(data_frame["Мастерская"] == master_select) & (data_frame["Группа"] == master_group) & \
                                  ((data_frame["Дата"] >= pd.to_datetime(str(start_period))) & (data_frame["Дата"] <= pd.to_datetime(str(end_period))))]

    productivity_plan = df_productivity["План"].sum()
    productivity_fact = df_productivity["Факт"].sum()
    percent_productivity = (productivity_fact / productivity_plan)

    if len(df_productivity) == 0:
        prize_to_productivity = 0
    else:
        if percent_productivity < 0.7:
            prize_to_productivity = 0
        elif percent_productivity >= 0.7 and percent_productivity <= 1.2:
            prize_to_productivity = percent_productivity
        elif percent_productivity > 1.2:
            prize_to_productivity = 1.2

    return prize_to_productivity

columns_1, columns_2 = st.columns(2)
columns_3, columns_4, columns_5 = st.columns(3)

with columns_1:
    departament_select = st.selectbox("Укажите департамент", position.keys()) # фильтр по управлению
with columns_2:
    master_select = st.selectbox("Укажите мастерскую", structure[departament_select])

with columns_3:
    master_group = st.selectbox("Укажите группу", structure[departament_select][master_select])
with columns_4:
    position_select = st.selectbox("Выберите должность", position[departament_select])
with columns_5:
    greid = st.selectbox("Выберите ваш грейд", greid_level.keys())

columns_6, columns_7, columns_8 = st.columns(3)

with columns_6:
    start_period = st.date_input("Укажите дату начала работы на должности", dt.datetime(2023,1,1), format="DD.MM.YYYY")
with columns_7:
    end_period = st.date_input("Укажите дату окончания работы на должности", dt.datetime.today(), format="DD.MM.YYYY")
with columns_8:
    salary_p1 = st.number_input("Укажите размер заработной платы: ", value=0, placeholder="Зарплата в рублях")

st.markdown("---")

calculate = st.button("Рассчитать премию", type="secondary")


delta = relativedelta.relativedelta(end_period, start_period)
salary_for_period = salary_p1 * delta.months + (salary_p1/30) * delta.days
prize_for_period = (salary_for_period * greid_level[greid])

delta_s = str(delta.months) + " / " + str(delta.days)

load_df, prize_to_load = load_status(df_load)
prize_to_izm = izm_status(df_izm)
prize_to_productivity = productivity_status(df_productivity)

bonus = prize_for_period*prize_to_load*0.35 + prize_for_period*prize_to_izm*0.35 + prize_for_period*prize_to_productivity*0.2

st.text(prize_to_load)
st.text(prize_to_izm)
st.text(prize_to_productivity)

text_1, text_2, text_3, text_4 = st.columns(4)
with text_1:
    st.metric(label="Отработано месяцев / дней", value=delta_s)
with text_2:
    st.metric(label="Заработная плата за период", value = round(salary_for_period, 2))
with text_3:
    st.metric(label="Размер целевой премии", value = round(prize_for_period, 2))
with text_4:
    st.metric(label="Премия с учетом выполнения показателей", value = round(bonus, 2))

    
