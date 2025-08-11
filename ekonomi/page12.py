import pandas as pd
import streamlit as st
import plotly.express as px


df = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 2", header = 1)

st.write(df)

st.subheader("Veri Filtreleme")

yillar = list(df["Yıl"])
yil_secimi = st.selectbox("Yıl Seçiniz:", ["Tümü"] + yillar)


kategoriler = list(df.columns)
kategoriler.remove("Yıl")
kategori_secimi = st.selectbox("Araç Türü Seçiniz:", ["Tümü"] + kategoriler)

df_filtered = df[df["Yıl"] == yil_secimi]


if kategori_secimi != "Tümü" and yil_secimi != "Tümü":
    fig = px.bar(df_filtered, x = "Yıl", y = kategori_secimi)
    st.plotly_chart(fig)

else:
    fig = px.bar(df, x = "Yıl", y = kategoriler)
    st.plotly_chart(fig)
