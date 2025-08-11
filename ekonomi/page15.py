from typing import Sized
import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 18", header = 1)
st.write(df)


sutunlar = list(df.columns)
sutunlar.remove("Yıl")

df["Yıl"] = df["Yıl"].astype(str)

# fig = px.bar(df, x="Yıl", y=sutunlar, barmode="group")
# st.plotly_chart(fig)



# fig = px.line(df, x = "Yıl", y = sutunlar)
# st.plotly_chart(fig)


col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(df, x="Yıl", y=sutunlar, barmode="group", width = 700)
    
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_line = px.line(df, x="Yıl", y=sutunlar)
    st.plotly_chart(fig_line, use_container_width=True)


