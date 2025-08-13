import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_excel("VerIstanbul.xlsx", sheet_name="Sheet 2", header=1)

st.markdown("<h1 style='text-align: center;'>Yıllara Göre Araç Sayısı ve Araç Sahipliği Oranı</h1>", unsafe_allow_html=True)
st.write(df)




st.markdown("<h2 style='text-align: center;'>BAR GRAFİĞİ</h2>", unsafe_allow_html=True)



col1, col2 = st.columns(2)

with col1:
    yillar = list(df["Yıl"].unique())
    yil_secimi = st.selectbox("Yıl Seçiniz:", ["Tümü"] + yillar)

with col2:
    kategoriler = list(df.columns)
    kategoriler.remove("Yıl")
    kategori_secimi = st.multiselect("Araç Türü Seçiniz:", options=kategoriler, default=kategoriler)


df_filtered = df.copy()

if yil_secimi != "Tümü":
    df_filtered = df_filtered[df_filtered["Yıl"] == yil_secimi]

if len(kategori_secimi) > 0:
    fig = px.bar(df_filtered, x="Yıl", y=kategori_secimi, height=800, color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_xaxes(dtick=1)

    fig.update_layout(
        xaxis_title="Yıl",
        yaxis_title="Araç Sayısı",
        legend_title_text=" ",
            legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=-0.3,             
            xanchor="center",
            x=0.5,
            font=dict(
                size=14,          
            ),
            itemwidth=30
        )
    )

    st.plotly_chart(fig)
else:
    st.warning("Lütfen en az bir araç türü seçiniz.")





st.markdown("<h2 style='text-align: center;'>AREA GRAFİĞİ</h2>", unsafe_allow_html=True)



df_long = df.melt(id_vars=["Yıl"], var_name="Araç Türü", value_name="Sayı")

fig = px.area(df_long, x="Yıl", y="Sayı", color="Araç Türü", line_group="Araç Türü", height=800, color_discrete_sequence=px.colors.sequential.Viridis)
fig.update_xaxes(dtick=1)
fig.update_layout(
    xaxis_title="Yıl",
    yaxis_title="Araç Sayısı",
    legend_title_text=" ",
    legend=dict(
        orientation="h",  
        yanchor="bottom",
        y=-0.3,             
        xanchor="center",
        x=0.5,
        font=dict(
            size=14,          
        ),
        itemwidth=30
    )
)
st.plotly_chart(fig)



st.markdown("<h2 style='text-align: center;'>YÜZDELİK DİLİM</h2>", unsafe_allow_html=True)


kategoriler = list(df.columns)
kategoriler.remove("Yıl")

yillar = sorted(df["Yıl"].unique())

col1, col2 = st.columns(2)

with col1:
    selected_years = st.multiselect(
        "Yıl Seçiniz:",
        options=yillar,
        default=yillar,
        key="year_multiselect"   
    )
with col2:
    selected_categories = st.multiselect(
        "Araç Türü Seçiniz:",
        options=kategoriler,
        default=kategoriler,
        key="category_multiselect"  
    )

if len(selected_years) == 0:
    st.warning("En az bir yıl seçmelisiniz!")
elif len(selected_categories) == 0:
    st.warning("En az bir araç türü seçmelisiniz!")
else:
    df_filtered = df[df["Yıl"].isin(selected_years)]

    df_toplam = df_filtered[selected_categories].sum().reset_index()
    df_toplam.columns = ["Araç Türü", "Toplam Sayı"]

    fig = px.pie(df_toplam, names="Araç Türü", values="Toplam Sayı", color_discrete_sequence=px.colors.sequential.Viridis)
            


    fig.update_layout(
        legend_title_text=" ",
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=-0.3,             
            xanchor="center",
            x=0.5,
            font=dict(
                size=14,          
            ),
            itemwidth=30
        )
    )

    st.plotly_chart(fig)



st.markdown("<h2 style='text-align: center;'>TREEMAP</h2>", unsafe_allow_html=True)



selected_year = st.selectbox("Yıl Seçiniz:", sorted(df_long["Yıl"].unique()))

df_filtered = df_long[df_long["Yıl"] == selected_year]


col1, col2 = st.columns([3,2])

with col1:
    fig = px.treemap(
        df_filtered,
        path=[px.Constant("Araçlar"), "Araç Türü"],
        values="Sayı",
        color="Sayı",
        color_continuous_scale="matter",
    )

    fig.update_traces(textinfo="label+value")

    fig.update_layout(
        coloraxis_colorbar=dict(
            orientation="h",
            thickness = 20,
            len = 1.2,
            y=-0.2,
            x=0.5,
            xanchor="center",
            yanchor="top"
        )
    )

    fig.update_coloraxes(colorbar_title="")
    st.plotly_chart(fig)



with col2:

    fig = px.sunburst(
        df_filtered,
        path=[px.Constant("Araçlar"), "Araç Türü"],
        values="Sayı",
        color="Sayı",
        color_continuous_scale="matter",
    )

    fig.update_traces(textinfo="label+value")

    fig.update_layout(
        coloraxis_colorbar=dict(
            orientation="h",
            thickness = 20,
            len = 0.8,
            y=-0.2,
            x=0.5,
            xanchor="center",
            yanchor="top"
        )
    )

    fig.update_coloraxes(colorbar_title="")

    st.plotly_chart(fig)
