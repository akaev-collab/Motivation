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
    "Выбирите данные", accept_multiple_files=False)
if uploaded_file is not None:
    file_name = uploaded_file
else:
    file_name = "data.xlsx"
