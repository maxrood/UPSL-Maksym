# 🔐 Aplikacja Streamlit do analizy ryzyka z bazą PostgreSQL

Aplikacja umożliwia ocenę ryzyk i zgodność z normami ISO/IEC 9126 oraz 27001. Dane ryzyk zapisywane są do zewnętrznej bazy PostgreSQL (np. Neon.tech).

## 🛠️ Instalacja lokalna

1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Utwórz zmienną środowiskową DATABASE_URL:
   export DATABASE_URL=postgresql://user:password@host:port/dbname

3. Uruchom aplikację:
   streamlit run app.py
