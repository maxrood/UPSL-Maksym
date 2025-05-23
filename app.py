import streamlit as st
from db import init_db, add_risk, get_risks
import matrix  # zakładamy, że masz wszystkie funkcje w module matrix.py

st.set_page_config(page_title="Zintegrowana analiza ryzyka", layout="wide")

# Inicjalizacja bazy danych
engine, Session = init_db()

st.title("📊 Zintegrowana analiza ryzyka z bazą PostgreSQL")

# Formularz dodawania nowego zagrożenia do bazy
st.subheader("➕ Dodaj zagrożenie do bazy danych")
with st.form("form_add_risk"):
    zagrozenie = st.text_input("Zagrożenie")
    prawdopodobienstwo = st.slider("Prawdopodobieństwo", 1, 5, 3)
    wplyw = st.slider("Wpływ", 1, 5, 3)
    submitted = st.form_submit_button("Zapisz do bazy")
    if submitted and zagrozenie.strip():
        add_risk(zagrozenie, prawdopodobienstwo, wplyw)
        st.success("Zagrożenie zapisane do bazy danych.")

# Wyświetlenie danych z bazy
st.subheader("📄 Istniejące ryzyka z bazy danych")
df = get_risks()
st.dataframe(df, use_container_width=True)

# Twoje pozostałe moduły (risk matrix, ISO/IEC 9126, ISO/IEC 27001)
st.divider()
matrix.main()  # zakładamy, że opakujesz swój kod w matrix.py w funkcję main()
