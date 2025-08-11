# import streamlit as st
# import pandas as pd
# st.subheader("Veri Seti")
# df = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 1", header = 1)
# st.write(df)



# st.subheader("Veri Filtreleme")

# fixed_column = "İlçeler"
# cols = df.columns.tolist()

# # selected_col = st.selectbox("Sütun Seçiniz: ", cols)

# # st.write(df[selected_col])




# other_cols = [col for col in cols if col != fixed_column]

# selected_col = st.multiselect("Sütun seçin", other_cols)

# if selected_col:
#     combined_df = pd.concat([df[[fixed_column]], df[selected_col]], axis=1)
#     st.write(combined_df)
# else:
#     st.info("Lütfen en az bir sütun seçin.")



import streamlit as st
import pandas as pd
import plotly.express as px

# Sayfa yapılandırması
st.set_page_config(page_title="İlçe Bazlı Kurumsal Yapılar", layout="wide")

# Veri yükleme
df = pd.read_excel("VerIstanbul.xlsx", sheet_name = "Sheet 1", header = 1)

st.title("📊 İstanbul İlçe Bazlı Kurumsal Yapılar")







# Sidebar - İlçe seçimi
ilce_sec = st.selectbox("İlçe Seçin", ["Tümü"] + list(df["İlçeler"].unique()))

if ilce_sec != "Tümü":
    filtered_df = df[df["İlçeler"] == ilce_sec]
else:
    filtered_df = df.copy()

# Ana gösterim
st.subheader(f"{ilce_sec} verileri" if ilce_sec != "Tümü" else "Tüm ilçeler")

st.dataframe(filtered_df, use_container_width=True)

# Grafik
st.subheader("📈 Kurum Dağılımı")
kurum_df = filtered_df.melt(id_vars="İlçeler", 
                            value_vars=["Üniversite Sayıları", "Teknopark Sayıları", "Vakıf Sayıları", "Dernek Sayıları"],
                            var_name="Kurum Türü", value_name="Sayı")

fig = px.bar(kurum_df, x="İlçeler", y="Sayı", color="Kurum Türü", barmode="group")
st.plotly_chart(fig, use_container_width=True)







st.title("İlçe Bazlı Kurum Dağılımı")



if not filtered_df.empty:
    kurumlar = ["Üniversite Sayıları", "Teknopark Sayıları", "Vakıf Sayıları", "Dernek Sayıları"]
    sayilar = [filtered_df[col].values[0] for col in kurumlar]

    pie_df = pd.DataFrame({
        "Kurum Türü": kurumlar,
        "Sayı": sayilar
    })

    fig = px.pie(pie_df, names="Kurum Türü", values="Sayı", title=f"{ilce_sec} Kurum Dağılımı")
    st.plotly_chart(fig)
else:
    st.warning("Seçilen ilçe bulunamadı.")









# Özet istatistik
st.subheader("📌 Toplam Kurum Sayıları")
toplamlar = filtered_df[["Üniversite Sayıları", "Teknopark Sayıları", "Vakıf Sayıları", "Dernek Sayıları"]].sum()
st.write(toplamlar.to_frame().rename(columns={0: "Toplam"}))
