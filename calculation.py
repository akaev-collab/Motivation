import streamlit as st
import numpy as np

st.set_page_config(layout="wide")
st.title("Калькулятор")
st.markdown("### Если за отчетный период был перевод просьба указать, если нет переходи к рассчету премии")
on = st.toggle("Был перевод")


