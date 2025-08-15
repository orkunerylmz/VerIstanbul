from streamlit_echarts import st_echarts
import pandas as pd
import streamlit as st
import plotly.express as px
import time


df = pd.read_excel("VerIstanbul.xlsx", sheet_name="Sheet 2", header=1)
df_long = df.melt(id_vars=["Yıl"], var_name="Araç Türü", value_name="Sayı")
kategoriler = list(df.columns)
kategoriler.remove("Yıl")
yillar = sorted(df["Yıl"].unique())

st.markdown("<h1 style='text-align: center;'>İstanbul Araç Analizi Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""

Bu dashboard, İstanbul’daki araç sayıları ve kategorileri üzerine kapsamlı bir analiz sunmaktadır. Şehirdeki otomobil, kamyon, motosiklet ve diğer araç türlerinin yıllara göre toplam sayıları bar grafiği ile görselleştirilmiş, belirli bir yıldaki araç türlerinin dağılımı pie grafiği ile gösterilmiş ve hem kategori hem de yıl bazlı detaylar treemap grafiği ile sunulmuştur.  

Bu görselleştirmeler sayesinde kullanıcılar;  
- Yıllar içindeki toplam araç sayısının değişim trendlerini,  
- Hangi araç türlerinin şehirde baskın olduğunu ve yıllara göre paylarının nasıl değiştiğini,  
- Araç kategorileri ve yıllar arasındaki hiyerarşik ilişkileri  

kolayca inceleyebilir. Dashboard, İstanbul’un trafik yoğunluğu, ulaşım altyapısı ve araç kullanım alışkanlıklarıyla ilgili veri temelli fikirler üretmek için tasarlanmıştır. Kullanıcılar, farklı grafikler arasındaki etkileşim sayesinde şehirdeki araç dağılımını daha detaylı analiz edebilir ve yıllık değişimleri karşılaştırabilir.
""")

with st.sidebar.expander("📅 Yıl ve Araç Türü Seçimi"):
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    selected_years = st.multiselect("Yıl Seçiniz:", options=yillar, default=years)
    selected_categories = st.multiselect("Araç Türü Seçiniz:", options=kategoriler, default=["Kamyon", "Minibüs", "Traktör"])

if len(selected_years) == 0:
    st.info("En az bir yıl seçmelisiniz!")
elif len(selected_categories) == 0:
    st.info("En az bir araç türü seçmelisiniz!")
else:

    df_filtered = df[df["Yıl"].isin(selected_years)]
    df_filtered_long = df_long[(df_long["Yıl"].isin(selected_years)) & (df_long["Araç Türü"].isin(selected_categories))]

    df_toplam = df_filtered[selected_categories].sum().reset_index()
    df_toplam.columns = ["Araç Türü", "Toplam Sayı"]
    df_sorted = df_toplam.sort_values("Toplam Sayı", ascending=False)
    categories = list(df_filtered_long["Araç Türü"].unique())


    if df_filtered.empty or df_filtered_long.empty:
        pass
        
    else:

        st.markdown("""
                    ### 📊 Piktogram Çubuk Grafiği - Araç Türlerine Göre Toplam Sayılar
                    ℹ️ Bu grafik, İstanbul’daki farklı araç türlerinin (otomobil, kamyon, motosiklet vb.) toplam sayılarını görselleştirmektedir. 
                    Her çubuk, ilgili araç türünün toplam sayısını temsil eder ve ikonlarla görselleştirilmiştir. 
                    Bu sayede hangi araç türlerinin şehirde daha yoğun olduğunu ve yıllar içindeki değişim trendlerini kolayca gözlemleyebilirsiniz.
                    """)



        option = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},

            "yAxis": {
                "data": df_sorted["Araç Türü"].tolist(),
                "inverse": True,
                "axisLine": {"show": False},
                "axisTick": {"show": False},
                "axisLabel": {"margin": 30, "fontSize": 14, "color": "white", "fontWeight": "bold"},
                "axisPointer": {"label": {"show": True, "fontSize": 14, "margin": 30, "fontWeight": "bold"}},
            },
            "xAxis": {
                "splitLine": {"show": False},
                "axisLabel": {"show": False},
                "axisTick": {"show": False},
                "axisLine": {"show": False},
            },
            "grid": {
                "left": "0%",    # Sol boşluk
                "right": "7%",   # Sağ boşluk
                "top": "2%",     # Üst boşluk
                "bottom": "1%",  # Alt boşluk
                "containLabel": True  # Eksen etiketlerinin dışarı taşmamasını sağlar
            },


            "color": [
                "rgb(127,110,181)",
                "rgb(154,131,201)",
                "rgb(180,153,216)",
                "rgb(203,176,228)",
                "rgb(223,200,238)",
                "rgb(158,151,194)"
            ],
            "series": [
                {
                    "name": "Toplam",
                    "type": "pictorialBar",
                    "data": df_sorted["Toplam Sayı"].tolist(),  # genel toplamlar burada
                    "label": {"show": True, "position": "right", "offset":[10, 0], "color": "white", "fontWeight": "extrabold"},
                    
                    "symbolRepeat": True,
                    "symbolSize": ["80%", "60%"],
                    "barCategoryGap": "40%",
                    "symbol": "path://M49.592,40.883c-0.053,0.354-0.139,0.697-0.268,0.963c-0.232,0.475-0.455,0.519-1.334,0.475 c-1.135-0.053-2.764,0-4.484,0.068c0,0.476,0.018,0.697,0.018,0.697c0.111,1.299,0.697,1.342,0.931,1.342h3.7 c0.326,0,0.628,0,0.861-0.154c0.301-0.196,0.43-0.772,0.543-1.78c0.017-0.146,0.025-0.336,0.033-0.56v-0.01 c0-0.068,0.008-0.154,0.008-0.25V41.58l0,0C49.6,41.348,49.6,41.09,49.592,40.883L49.592,40.883z M6.057,40.883 c0.053,0.354,0.137,0.697,0.268,0.963c0.23,0.475,0.455,0.519,1.334,0.475c1.137-0.053,2.762,0,4.484,0.068 c0,0.476-0.018,0.697-0.018,0.697c-0.111,1.299-0.697,1.342-0.93,1.342h-3.7c-0.328,0-0.602,0-0.861-0.154 c-0.309-0.18-0.43-0.772-0.541-1.78c-0.018-0.146-0.027-0.336-0.035-0.56v-0.01c0-0.068-0.008-0.154-0.008-0.25V41.58l0,0 C6.057,41.348,6.057,41.09,6.057,40.883L6.057,40.883z M49.867,32.766c0-2.642-0.344-5.224-0.482-5.507 c-0.104-0.207-0.766-0.749-2.271-1.773c-1.522-1.042-1.487-0.887-1.766-1.566c0.25-0.078,0.492-0.224,0.639-0.241 c0.326-0.034,0.345,0.274,1.023,0.274c0.68,0,2.152-0.18,2.453-0.48c0.301-0.303,0.396-0.405,0.396-0.672 c0-0.268-0.156-0.818-0.447-1.146c-0.293-0.327-1.541-0.49-2.273-0.585c-0.729-0.095-0.834,0-1.022,0.121 c-0.304,0.189-0.32,1.919-0.32,1.919l-0.713,0.018c-0.465-1.146-1.11-3.452-2.117-5.269c-1.103-1.979-2.256-2.599-2.737-2.754 c-0.474-0.146-0.904-0.249-4.131-0.576c-3.298-0.344-5.922-0.388-8.262-0.388c-2.342,0-4.967,0.052-8.264,0.388 c-3.229,0.336-3.66,0.43-4.133,0.576s-1.633,0.775-2.736,2.754c-1.006,1.816-1.652,4.123-2.117,5.269L9.87,23.109 c0,0-0.008-1.729-0.318-1.919c-0.189-0.121-0.293-0.225-1.023-0.121c-0.732,0.104-1.98,0.258-2.273,0.585 c-0.293,0.327-0.447,0.878-0.447,1.146c0,0.267,0.094,0.379,0.396,0.672c0.301,0.301,1.773,0.48,2.453,0.48 c0.68,0,0.697-0.309,1.023-0.274c0.146,0.018,0.396,0.163,0.637,0.241c-0.283,0.68-0.24,0.524-1.764,1.566 c-1.506,1.033-2.178,1.566-2.271,1.773c-0.139,0.283-0.482,2.865-0.482,5.508s0.189,5.02,0.189,5.86c0,0.354,0,0.976,0.076,1.565 c0.053,0.354,0.129,0.697,0.268,0.966c0.232,0.473,0.447,0.516,1.334,0.473c1.137-0.051,2.779,0,4.477,0.07 c1.135,0.043,2.297,0.086,3.33,0.11c2.582,0.051,1.826-0.379,2.928-0.36c1.102,0.016,5.447,0.196,9.424,0.196 c3.976,0,8.332-0.182,9.423-0.196c1.102-0.019,0.346,0.411,2.926,0.36c1.033-0.018,2.195-0.067,3.332-0.11 c1.695-0.062,3.348-0.121,4.477-0.07c0.886,0.043,1.103,0,1.332-0.473c0.132-0.269,0.218-0.611,0.269-0.966 c0.086-0.592,0.078-1.213,0.078-1.565C49.678,37.793,49.867,35.408,49.867,32.766L49.867,32.766z M13.219,19.735 c0.412-0.964,1.652-2.9,2.256-3.244c0.145-0.087,1.426-0.491,4.637-0.706c2.953-0.198,6.217-0.276,7.73-0.276 c1.513,0,4.777,0.078,7.729,0.276c3.201,0.215,4.502,0.611,4.639,0.706c0.775,0.533,1.842,2.28,2.256,3.244 c0.412,0.965,0.965,2.858,0.861,3.116c-0.104,0.258,0.104,0.388-1.291,0.275c-1.387-0.103-10.088-0.216-14.185-0.216 c-4.088,0-12.789,0.113-14.184,0.216c-1.395,0.104-1.188-0.018-1.291-0.275C12.254,22.593,12.805,20.708,13.219,19.735 L13.219,19.735z M16.385,30.511c-0.619,0.155-0.988,0.491-1.764,0.482c-0.775,0-2.867-0.353-3.314-0.371 c-0.447-0.017-0.842,0.302-1.076,0.362c-0.23,0.06-0.688-0.104-1.377-0.318c-0.688-0.216-1.092-0.155-1.316-1.094 c-0.232-0.93,0-2.264,0-2.264c1.488-0.068,2.928,0.069,5.621,0.826c2.693,0.758,4.191,2.213,4.191,2.213 S17.004,30.357,16.385,30.511L16.385,30.511z M36.629,37.293c-1.23,0.164-6.386,0.207-8.794,0.207c-2.412,0-7.566-0.051-8.799-0.207 c-1.256-0.164-2.891-1.67-1.764-2.865c1.523-1.627,1.24-1.576,4.701-2.023C24.967,32.018,27.239,32,27.834,32 c0.584,0,2.865,0.025,5.859,0.404c3.461,0.447,3.178,0.396,4.699,2.022C39.521,35.623,37.887,37.129,36.629,37.293L36.629,37.293z  M48.129,29.582c-0.232,0.93-0.629,0.878-1.318,1.093c-0.688,0.216-1.145,0.371-1.377,0.319c-0.231-0.053-0.627-0.371-1.074-0.361 c-0.448,0.018-2.539,0.37-3.313,0.37c-0.772,0-1.146-0.328-1.764-0.481c-0.621-0.154-0.966-0.154-0.966-0.154 s1.49-1.464,4.191-2.213c2.693-0.758,4.131-0.895,5.621-0.826C48.129,27.309,48.361,28.643,48.129,29.582L48.129,29.582z",
                }
            ],
        }


        tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])


        with tab2:
            st.dataframe(df_toplam)

        with tab1:
            st_echarts(option, height="750px")


        st.markdown("""

                    ### 📈 Bar Grafiği - Yıllara Göre Toplam Araç Sayısı
                    ℹ️ Bu grafik, İstanbul’daki tüm araç kategorilerinin (otomobil, kamyon, motosiklet vb.) yıllık toplam sayısını göstermektedir. 
                    Her çubuk, o yıla ait tüm araçların toplamını temsil eder ve yıllar içindeki değişimi görselleştirir. 
                    Bu sayede şehirdeki araç yoğunluğunun artış veya azalış trendlerini kolayca takip edebilirsiniz.""")



        # Her kategorinin toplamını hesapla ve sırala
        cat_totals = df_filtered[categories].sum().sort_values(ascending=False)
        sorted_categories = cat_totals.index.tolist()

        # Renk paleti (en yüksek toplamdan başlayacak şekilde)
        color_palette = [
            "rgb(97,88,154)",
            "rgb(127,110,181)",
            "rgb(154,131,201)",
            "rgb(180,153,216)",
            "rgb(203,176,228)",
            "rgb(223,200,238)",
            "rgb(240,225,245)",
            "rgb(158,151,194)"
        ]

        # ECharts için veri hazırlama
        series_data = []
        for i, cat in enumerate(sorted_categories):
            series_data.append({
                "name": cat,
                "type": "bar",
                "stack": "total",
                "label": {"show": False},
                "emphasis": {"focus": "series"},
                "itemStyle": {"color": color_palette[i % len(color_palette)]},
                "data": df_filtered[cat].astype(int).tolist()
            })

        option = {
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {
                "data": sorted_categories,
                "orient": "horizontal",
                "bottom": 0,
                "textStyle": {"fontSize": 14, "color": "white", "fontWeight": "bold"},
                
            },
            "grid": {"left": "0%", "right": "0%", "bottom": "15%", "containLabel": True},
            "xAxis": {"type": "category", "data": df_filtered["Yıl"].tolist()}, "axisLabel": {"color": "white", "fontWeight": "bold"},
            "yAxis": {"type": "value", "name": "Araç Sayısı", "axisLabel": {"color": "white", "fontWeight": "bold"}, "nameGap": 30, "nameTextStyle": {"color": "white", "fontSize": 16, "fontWeight": "bold"}},
            "series": series_data,
        }




        tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])


        with tab2:
            st.dataframe(df_filtered_long)

        with tab1:
            st_echarts(option, height="700px")


        st.markdown("""
                    ## 📊 Alan Grafiği - Yıllara Göre Toplam Araç Sayısı
                    ℹ️ Bu grafik, İstanbul’daki tüm araç kategorilerinin yıllara göre toplam sayısını alan grafiği ile görselleştirir. 
                    Grafikteki alanın büyüklüğü, her yıl içindeki toplam araç miktarını temsil eder ve zaman içindeki değişimleri net bir şekilde ortaya koyar. 
                    Yıllar içindeki artış ve azalış trendlerini görmek, trafik yoğunluğu ve araç kullanımındaki değişimleri analiz etmek için uygundur.
                    """)




        vehicles = df_filtered_long["Araç Türü"].unique().tolist()
        years = sorted(df_filtered_long["Yıl"].unique())

        colors = [
            "rgb(97,88,154)",
            "rgb(127,110,181)",
            "rgb(154,131,201)",
            "rgb(180,153,216)",
            "rgb(203,176,228)",
            "rgb(223,200,238)",
            "rgb(240,225,245)",
            "rgb(158,151,194)"
        ]
        colors = colors[:len(vehicles)]
        colors = sorted(colors, reverse=True)

        series_data = []
        for idx, vehicle in enumerate(vehicles):
            counts = df_filtered_long[df_filtered_long["Araç Türü"] == vehicle]["Sayı"].tolist()
            counts = [int(c) for c in counts]
            series_data.append({
                "name": vehicle,
                "type": "line",
                "stack": "total",
                "areaStyle": {"color": colors[idx]},
                "lineStyle": {"color": colors[idx], "width": 2},
                "symbol": "circle",            # Noktaları geri ekledik
                "symbolSize": 6,               # Nokta boyutu
                "itemStyle": {"color": colors[idx]},  # Noktaları çizgi rengiyle eşle
                "emphasis": {"focus": "series"},
                "data": counts
            })

        option_area = {
            "tooltip": {"trigger": "axis"},
            "legend": {
                "data": vehicles,
                "bottom": "5%",
                "left": "center",
                "textStyle": {"color": "white", "fontWeight": "bold"}  # Yazılar beyaz
            },

            "grid": {
                "left": "0%",    # Sol boşluk
                "right": "0%",   # Sağ boşluk
                "top": "10%",     # Üst boşluk
                "bottom": "15%",  # Alt boşluk
                "containLabel": True  # Eksen etiketlerinin dışarı taşmamasını sağlar
            },

            "xAxis": {
                "type": "category",
                "data": [int(y) for y in years],
                "axisLabel": {"color": "white", "fontWeight": "bold"}
            },
            "yAxis": {
                "type": "value",
                "name": "Araç Sayısı",
                "nameGap": 35, 
                "nameTextStyle": {"color": "white", "fontSize": 16, "fontWeight": "bold"},
                "axisLabel": {"color": "white", "fontWeight": "bold"}
            },
            "series": series_data,
        }






        tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])
        with tab2:
            st.dataframe(df_filtered_long)
        with tab1:
            st_echarts(option_area, height="700px")


        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                        ### 🥧 Pasta Grafiği - Araç Kategorilerinin Payı
                        ℹ️ Bu grafik, seçilen bir yıldaki farklı araç türlerinin toplam araç sayısı içindeki yüzdesel dağılımını gösterir. 
                        Her dilim, ilgili araç kategorisinin şehirdeki payını temsil eder. 
                        Bu sayede hangi araç türlerinin baskın olduğunu ve kategori dağılımını hızlı bir şekilde görebilirsiniz.
                        """)

        with col2:
            st.markdown("""
                        ### 🌞 Hiyerarşik Grafik - Kategori Bazlı Araç Dağılımı
                        ℹ️ Bu grafik, araç kategorilerini ve yıllarını hiyerarşik olarak bir araya getirir. 
                        Daire içindeki katmanlar, kategori ve yıl ilişkilerini gösterirken, alan büyüklükleri araç sayısını temsil eder. 
                        Hem kategori hem de zaman bazlı analizler yapmak ve değişimleri detaylı bir şekilde karşılaştırmak için idealdir.
                        """)


        options = {
            "tooltip": {"trigger": "item"},
            "legend": {
                "orient": "horizontal",
                "bottom": 0,
                "itemGap": 10,
                "textStyle": {
                    "color": "white",   # Legend yazıları beyaz
                    "fontWeight": "bold"
                }
            },

            "color": [
                "rgb(97,88,154)",
                "rgb(127,110,181)",
                "rgb(154,131,201)",
                "rgb(180,153,216)",
                "rgb(203,176,228)",
                "rgb(223,200,238)",
                "rgb(240,225,245)",
                "rgb(158,151,194)"
            ],
            "series": [
                {
                    "name": "Araç Türü",
                    "type": "pie",
                    "radius": "85%",
                    "data": [{"value": v, "name": n} for n, v in zip(df_sorted["Araç Türü"], df_sorted["Toplam Sayı"])],
                    
                    # Label ve çizgileri kapat
                    "label": {
                        "show": True,  
                        "position": "inside",        # Labeli aç
                        "formatter": "{d}%",   # Yüzdelik göster
                        "color": "white",      # Yazı rengi
                        "fontWeight": "bold"   # Kalın
                    },
                    "labelLine": {"show": False},
                    
                    # Hover sırasında da label çıkmasın
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)"
                        },
                        "label": {"show": False},         # Hover yazısını kapat
                        "labelLine": {"show": False}      # Hover çizgisini kapat
                    },
                    
                    "animationDuration": 1500,
                    "animationEasing": "cubicOut"
                }
            ]

        }
        events = {
            "legendselectchanged": "function(params) { return params.selected }",
        }

        col1, col2 = st.columns(2)

        with col1:
            tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])
            with tab1:
                selected = st_echarts(options=options, events=events, height="700px", key="pie_chart")
                
            with tab2:
                st.dataframe(df_toplam)

        fig_sun = px.sunburst(df_filtered_long, path=[px.Constant("Araçlar"), "Araç Türü"], values="Sayı", color="Sayı", color_continuous_scale="purp", height = 700)

        fig_sun.update_traces(textinfo="label+value")
        fig_sun.update_layout(coloraxis_colorbar=dict(orientation="v", thickness=20, len=0.8, y=0.5, x=1.02, xanchor="left", yanchor="middle"), coloraxis_showscale=False)

        with col2:
            tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])
            with tab1:
                st.plotly_chart(fig_sun, use_container_width=True)

            with tab2:
                st.dataframe(df_filtered_long)

        st.markdown("""
                    ### 🗂️ Ağaç Haritası – Araç Kategorileri ve Yıllık Dağılım
                    ℹ️ Bu grafik, her araç kategorisinin seçilen yıllardaki büyüklüğünü ve toplam araç sayısındaki payını hiyerarşik bir yapıda sunar. 
                    Alanların büyüklüğü araç sayısını, renk tonları ise aynı değeri yoğunluk farkıyla gösterir. 
                    Böylece hem kategori bazında hem de değer büyüklüğü açısından görsel bir karşılaştırma yapılabilir.
        """)

        df_tree = df_filtered_long[df_filtered_long["Yıl"].isin(selected_years)]

        fig_tree = px.treemap(df_tree, path=[px.Constant("Araçlar"), "Araç Türü"], values="Sayı", color="Sayı", color_continuous_scale="purp", height=700)  
        fig_tree.update_traces(textinfo="label+value")  
        fig_tree.update_layout(coloraxis_colorbar=dict(orientation="h", thickness=20, len=1.2, y=-0.03, x=0.5, xanchor="center", yanchor="top"), coloraxis_colorbar_title_text="")  

        tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])

        with tab2:
            st.dataframe(df_tree)

        with tab1:
            st.plotly_chart(fig_tree, use_container_width=True)


        st.markdown("""
                    ### 🗂️ Ağaç Haritası – Seçili Yıllar ve Araç Kategorileri
                    ℹ️ Bu grafik, seçilen yıllardaki araç kategorilerini hiyerarşik bir yapıda görselleştirir. 
                    Her bir düğümün alanı, ilgili kategori veya yıl için araç sayısını temsil eder; renk tonları ise aynı değeri yoğunluk farkıyla vurgular.  
                    - **Root düğüm**: Seçili yılların toplam araç sayısını gösterir,  
                    - **Yıl düğümleri**: O yıla ait toplam araç sayısını belirtir,  
                    - **Kategori düğümleri**: Her kategoriye ait araç sayısını gösterir.  

                    Bu sayede hem yıllar hem de kategoriler bazında araç sayılarının dağılımını ve büyüklük farklarını kolayca karşılaştırabilirsiniz.
                    """)

        toplam_secili_yillar = df_filtered_long["Sayı"].sum()

        data = {"name": "Araçlar", "tooltip": {"formatter": f"{toplam_secili_yillar}"}, "children": []}
        for yil in df_filtered_long["Yıl"].unique():
            df_yil = df_filtered_long[df_filtered_long["Yıl"] == yil]
            toplam_yil = df_yil["Sayı"].sum()
            children = []
            for _, row in df_yil.iterrows():
                children.append({
                    "name": row["Araç Türü"],
                    "value": row["Sayı"],
                    "tooltip": {"formatter": f"{row['Sayı']}"}
                })
            data["children"].append({
                "name": str(yil),
                "tooltip": {"formatter": f"{toplam_yil}"},  
                "children": children
            })

        option = {
            "tooltip": {
                "trigger": "item",
                "formatter": """function(params){
                    return params.data.tooltip ? params.data.tooltip.formatter : params.name;
                }"""
            },
            "series": [
                {
                    "type": "tree",
                    "data": [data],
                    "top": "5%",
                    "left": "10%",
                    "bottom": "5%",
                    "right": "10%",
                    "symbolSize": 15,
                    "levelDistance": 10,  
                    "orient": "horizontal",  
                    "layout": "orthogonal",  

                    "label": {
                        "position": "left",
                        "verticalAlign": "middle",
                        "align": "right",
                        "color": "white",
                        "fontWeight": "bold",
                        "fontSize": 12,
                    },
                    "leaves": {
                        "label": {
                            "position": "right",
                            "verticalAlign": "middle",
                            "align": "left",
                        }
                    },
                    "emphasis": {"focus": "descendant"},
                    "expandAndCollapse": True,
                    "animationDuration": 550,
                    "animationDurationUpdate": 750,
                }
            ]
        }

        tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])

        with tab2:
            st.dataframe(df_tree)

        with tab1:
            st_echarts(option, height="600px")


        years = sorted(df_filtered_long["Yıl"].unique())

        data = []
        for i, category in enumerate(categories):
            for j, year in enumerate(years):
                val = df_filtered_long.loc[
                    (df_filtered_long["Yıl"] == year) & (df_filtered_long["Araç Türü"] == category),
                    "Sayı"
                ].sum()
                val = int(val)  # <- burası kesin Python int
                data.append([j, i, val])

        option = {
            "tooltip": {"position": "top"},
            "grid": {"height": "70%", "top": "7%"},
            "xAxis": {"type": "category", "data": [str(y) for y in years], "splitArea": {"show": True}, "axisLabel": {"color": "white", "fontWeight": "bold"}},
            "yAxis": {"type": "category", "data": categories, "splitArea": {"show": True}, "axisLabel": {"color": "white", "fontWeight": "bold"}},
            "visualMap": {
                "min": 0,
                "max": max(d[2] for d in data),
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "10%",
                "len": 1,   
                "inRange": {
                    "color": [
            
                        "rgb(240,225,245)",
                        "rgb(203,176,228)",
                        "rgb(97,88,154)",
                    ]

                },
                "textStyle": {"color": "white", "fontWeight": "bold"},  # sayı rengini beyaz yap

            },

            "label": {"fontSize": 14, "fontWeight": "bold"},
            "series": [
                {
                    "name": "Araç Sayısı",
                    "type": "heatmap",
                    "data": data,
                    "label": {"show": True},
                    "emphasis": {
                        "itemStyle": {"shadowBlur": 10, "shadowColor": "rgba(0, 0, 0, 0.5)"}
                    },
                }
            ],
        }

        st.markdown("""
        ### 🌡️ Isı Haritası - Yıl ve Araç Kategorisine Göre Araç Sayısı 
        ℹ️ Bu grafik, seçili yıllara ait araç sayılarını araç kategorileri bazında görselleştirir. 
                    X ekseni yılları, Y ekseni ise araç kategorilerini temsil eder. Her hücre, belirli bir kategoriye ait araç sayısını gösterir ve hücrenin rengi bu sayının yoğunluğunu yansıtır.  
        - **Hücre renkleri**: Araç sayısı yoğunluğu  
        - **Renk skalası (VisualMap)**: Alttaki çubuk, hangi renk tonunun hangi araç sayısına karşılık geldiğini gösterir.  

        Bu sayede, hangi araç kategorisinin hangi yılda ne kadar yoğun olduğunu hızlıca görselleştirebilir ve trendleri kolayca karşılaştırabilirsiniz.
        """)


        tab1, tab2 = st.tabs(["📊 Grafik", "📄 Veri"])

        with tab2:
            st.dataframe(df_tree)

        with tab1:

            st_echarts(option, height="700px")






