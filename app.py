import streamlit as st


st.set_page_config(
    page_title="VerIstanbul",
    layout="wide",       
    initial_sidebar_state="expanded"
)

page1 = st.Page("VerIstanbul/anasayfa.py", title = "Ana Sayfa", icon = ":material/home:", default=True)
page2 = st.Page("VerIstanbul/iletisim.py", title = "İletişim", icon = ":material/mail:")

page10 = st.Page("ekonomi/page10.py", title="İlçe Bazlı Veriler", icon = ":material/payments:")
page11 = st.Page("ekonomi/page11.py", title="Gelir Dağılımı", icon = ":material/payments:")
page12 = st.Page("ekonomi/page12.py", title="Araç Sayısı ve Araç Sahiplik Oranı", icon = ":material/payments:")
page13 = st.Page("ekonomi/page13.py", title="Endeksler", icon = ":material/payments:")
page14 = st.Page("ekonomi/page14.py", title="Fiber Optik Haberleşme Sistemi ve Altyapı", icon = ":material/payments:")
page15 = st.Page("ekonomi/page15.py", title="Girişimler ve Girişimciler", icon = ":material/payments:")
page16 = st.Page("ekonomi/page16.py", title="GSYH ve Kişi Başı GSYH", icon = ":material/payments:")
page17 = st.Page("ekonomi/page17.py", title="İşsizlik ve İstihdam", icon = ":material/payments:")
page18 = st.Page("ekonomi/page18.py", title="Ruhsatlı İşyeri Sayısı", icon = ":material/payments:")
page19 = st.Page("ekonomi/page19.py", title="Teknoloji", icon = ":material/payments:")
page20 = st.Page("ekonomi/page20.py", title="Yatırım ve Sermaye", icon = ":material/payments:")

page30 = st.Page("sosyal/page30.py", title="Nüfus", icon=":material/people:")
page31 = st.Page("sosyal/page31.py", title="History", icon=":material/people:")

pg = st.navigation(
    {
        "VerIstanbul": [page1, page2],
        "Ekonomi": [page10, page11, page12, page13, page14, page15, page16, page17, page18, page19, page20],
        "Sosyal": [page30, page31],
    }
)

pg.run()