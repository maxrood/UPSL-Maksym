import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Analiza ryzyka", layout="wide")
st.title("🔐 Analiza ryzyka systemów teleinformatycznych")

# === ISTNIEJĄCY MODUŁ: Analiza ryzyka ===
def klasyfikuj_ryzyko(poziom):
    if poziom <= 6:
        return "Niskie"
    elif poziom <= 14:
        return "Średnie"
    else:
        return "Wysokie"

default_risks = [
    {"Zagrożenie": "Awaria serwera", "Prawdopodobieństwo": 4, "Wpływ": 5},
    {"Zagrożenie": "Atak DDoS", "Prawdopodobieństwo": 3, "Wpływ": 4},
    {"Zagrożenie": "Błąd ludzki", "Prawdopodobieństwo": 5, "Wpływ": 3},
    {"Zagrożenie": "Utrata zasilania", "Prawdopodobieństwo": 2, "Wpływ": 2}
]

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(default_risks)

st.subheader("➕ Dodaj nowe zagrożenie")
with st.form("add_risk_form"):
    name = st.text_input("Opis zagrożenia")
    prob = st.slider("Prawdopodobieństwo (1-5)", 1, 5, 3)
    impact = st.slider("Wpływ (1-5)", 1, 5, 3)
    submitted = st.form_submit_button("Dodaj")
    if submitted and name.strip() != "":
        new_row = {"Zagrożenie": name, "Prawdopodobieństwo": prob, "Wpływ": impact}
        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Zagrożenie dodane.")

st.subheader("✏️ Edytuj macierz ryzyka")
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, key="risk_editor")
st.session_state.df = edited_df.copy()

edited_df["Poziom ryzyka"] = edited_df["Prawdopodobieństwo"] * edited_df["Wpływ"]
edited_df["Klasyfikacja"] = edited_df["Poziom ryzyka"].apply(klasyfikuj_ryzyko)

st.subheader("📋 Filtruj według poziomu ryzyka")
filt = st.radio("Pokaż:", ["Wszystkie", "Niskie", "Średnie", "Wysokie"], horizontal=True)
df_filtered = edited_df if filt == "Wszystkie" else edited_df[edited_df["Klasyfikacja"] == filt]

def koloruj(val):
    return {
        "Niskie": "background-color: #d4edda",
        "Średnie": "background-color: #fff3cd",
        "Wysokie": "background-color: #f8d7da"
    }.get(val, "")

st.subheader("📊 Macierz ryzyka")
st.dataframe(df_filtered.style.applymap(koloruj, subset=["Klasyfikacja"]), use_container_width=True)

# === NOWY MODUŁ: ISO/IEC 9126 ===
st.header("📐 Ocena jakości systemu wg ISO/IEC 9126")

cechy = ["Funkcjonalność", "Niezawodność", "Użyteczność", "Wydajność", "Możliwość konserwacji", "Przenośność"]
oceny = {}
cols = st.columns(len(cechy))

for i, cecha in enumerate(cechy):
    with cols[i]:
        oceny[cecha] = st.slider(cecha, 1, 5, 3)

df_9126 = pd.DataFrame(oceny, index=["Ocena"])
srednia = df_9126.loc["Ocena"].mean()

st.subheader("📈 Wyniki ISO/IEC 9126")
st.write(f"Średnia ocena: **{srednia:.2f}**")
interpretacja = "Wysoka jakość" if srednia >= 4 else "Średnia jakość" if srednia >= 3 else "Niska jakość"
st.success(f"🧠 Interpretacja: Twoja aplikacja wykazuje **{interpretacja}** ogólną jakość.")

if st.checkbox("📊 Pokaż wykres radarowy"):
    fig = px.line_polar(r=df_9126.loc["Ocena"], theta=cechy, line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

# === NOWY MODUŁ: ISO/IEC 27001 ===
st.header("🛡️ Ocena zgodności z normą ISO/IEC 27001")

obszary = {
    "Organizacyjne (A.5)": ["Polityka bezpieczeństwa", "Zarządzanie ryzykiem", "Zarządzanie zasobami"],
    "Ludzkie (A.6)": ["Szkolenia z bezpieczeństwa", "Uprawnienia pracowników", "Rozdzielność obowiązków"],
    "Fizyczne (A.7)": ["Dostęp fizyczny", "Zabezpieczenia sprzętu", "Ochrona przed katastrofami"],
    "Techniczne (A.8)": ["Zarządzanie tożsamością i dostępem", "Szyfrowanie danych", "Monitoring i logowanie"]
}

obszar = st.selectbox("Wybierz obszar kontroli bezpieczeństwa", list(obszary.keys()))
oceny_27001 = {}
st.subheader(f"🧪 Ocena kontroli – {obszar}")
for kontrola in obszary[obszar]:
    oceny_27001[kontrola] = st.slider(kontrola, 1, 5, 3)

df_27001 = pd.DataFrame(oceny_27001, index=["Ocena"])
srednia_27001 = df_27001.loc["Ocena"].mean()
kolor = "🟢" if srednia_27001 >= 4 else "🟡" if srednia_27001 >= 2.5 else "🔴"

st.subheader("📉 Podsumowanie zgodności")
st.write(f"{kolor} Średni poziom wdrożenia: **{srednia_27001:.2f}**")

if srednia_27001 >= 4:
    interpretacja_27001 = "bardzo dobrze wdrożony"
elif srednia_27001 >= 2.5:
    interpretacja_27001 = "częściowo wdrożony – wymaga poprawek"
else:
    interpretacja_27001 = "niewystarczająco wdrożony – konieczne działania"

st.info(f"📌 Obszar **{obszar}** jest **{interpretacja_27001}**.")
