import pandas as pd
import streamlit as st

st.title("New page")

data = pd.DataFrame({"a":[1,24,3], 'b':[2,45,34]})

data_1 = pd.read_csv(data, sep = ";")

st.dataframe(data)
st.dataframe(data_1)

st.text("new line")
