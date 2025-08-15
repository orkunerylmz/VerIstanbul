from typing import Sized
import pandas as pd
import plotly.express as px
import streamlit as st


df1 = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 18", header = 1)
df2 = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 20", header = 1)
st.write(df1)
st.write(df2)



# Uzun başlıkları satır kırma ile kısaltma
df2["Kategoriler"] = df2["Kategoriler"].apply(lambda x: "<br>".join(x.split(" ")))

fig = px.bar(
    df2,
    x="Kategoriler",
    y="Girişim Sayıları",
    height=800,
    color_discrete_sequence=px.colors.sequential.Purp_r
)

# Başlıkları düz (yatay) yap
fig.update_xaxes(tickangle=0, tickfont=dict(size=8))
fig.update_yaxes(title_text="Girişim Sayısı")

fig.update_layout(
    xaxis_title="",
    bargap=0.3
)

st.plotly_chart(fig, use_container_width=True)

