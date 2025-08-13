import pandas as pd
import streamlit as st
import plotly.express as px


df = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 12", header = 1)
st.write(df)


df_long = df.melt(id_vars="ÜLKE", var_name="Yatırımlar", value_name="Sayı")


fig = px.treemap(df_long, path=["ÜLKE", "Yatırımlar"], values= "Sayı", color = "Sayı", color_continuous_scale="matter")





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




fig = px.area(df, x = "ÜLKE", y = "YABANCI YATIRIMCI SAYISI", color = "YABANCI SERMAYE (TL)", height = 1000)
st.plotly_chart(fig)









df_sort = df.sort_values(by="YABANCI YATIRIMCI SAYISI", ascending=False)
fig = px.funnel(df_sort, x = "YABANCI YATIRIMCI SAYISI", y = "ÜLKE", title = "YATIRIMCI")
fig.update_layout(
    title_text="YABANCI YATIRIMCI",
    title_x=0.5, 
)



fig.update_traces(
    marker=dict(color="skyblue"),
    texttemplate='%{x:.2s}',
    textposition='inside',
    marker_line_color="black",
    hovertemplate='Ülke: %{y}<br>Yatırımcı Sayısı: %{x}<extra></extra>'
)

fig.update_layout(
    width=900,
    height=600,
)


st.plotly_chart(fig)






df_sort = df.sort_values(by="YABANCI SERMAYE (TL)", ascending=False)
fig = px.funnel(df_sort, x = "YABANCI SERMAYE (TL)", y = "ÜLKE", title = "SERMAYE")

fig.update_layout(
    title_text="YABANCI SERMAYE",
    title_x=0.5, 
)


fig.update_traces(
    marker=dict(color="skyblue"),
    
    texttemplate='%{x:.2s}',
    textposition='inside',
    marker_line_color="black",
    hovertemplate='Ülke: %{y}<br>Sermaye: %{x}<extra></extra>'
)

fig.update_layout(
    width=900,
    height=600,
    template='plotly_white',
    font=dict(family="Arial", size=14, color="black")
)





st.plotly_chart(fig)
