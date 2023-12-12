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

df_load = pd.read_excel('data.xlsx', sheet_name="P_RD")

st.dataframe(df_load)
