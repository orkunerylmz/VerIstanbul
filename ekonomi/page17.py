from typing import Sized
import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 19", header = 1)
st.write(df)



col1, col2 = st.columns(2)

with col1:
    fig_donut = px.pie(df, names="Sektör", values="Yüzdelik Dilim", hole=0.4, title="Sektörlerin Pazar Payı (Donut)")
    st.plotly_chart(fig_donut, use_container_width = True)


with col2:
    fig = px.bar(df, x="Sektör", y="Yüzdelik Dilim", title="İstihdamın Sektörel Dağılımı")
    st.plotly_chart(fig, use_container_width = True)
