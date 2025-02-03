import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Titel des Dashboards
st.title("Projekt Performance Reporting Dashboard")

# 1. Beispiel-Daten: Projektfortschritt über die Zeit
# Erstellen eines DataFrame mit Datum, geplantem und tatsächlichem Fortschritt
data = {
    "Datum": pd.date_range(start="2025-01-01", periods=10, freq="W"),
    "Geplanter Fortschritt (%)": np.linspace(0, 100, 10),
    "Tatsächlicher Fortschritt (%)": np.linspace(0, 90, 10) + np.random.uniform(-5, 5, 10)
}
df_progress = pd.DataFrame(data)

# Diagramm: Projektfortschritt
fig_progress = px.line(df_progress, x="Datum", y=["Geplanter Fortschritt (%)", "Tatsächlicher Fortschritt (%)"],
                         title="Projektfortschritt im Zeitverlauf")
st.plotly_chart(fig_progress)

# 2. Beispiel-Daten: Budgetstatus
budget_data = {
    "Kategorie": ["Gesamtbudget", "Ausgegeben"],
    "Betrag (€)": [100000, 75000]
}
df_budget = pd.DataFrame(budget_data)

# Diagramm: Budgetstatus als Tortendiagramm
fig_budget = px.pie(df_budget, names="Kategorie", values="Betrag (€)", title="Budgetstatus")
st.plotly_chart(fig_budget)

# 3. Anzeige von Kennzahlen (KPIs)
st.subheader("Kennzahlen")

# Annahmen für KPIs (diese Werte können später dynamisch aus deinen Daten berechnet werden)
aktueller_fortschritt = df_progress["Tatsächlicher Fortschritt (%)"].iloc[-1]
geplanter_fortschritt = df_progress["Geplanter Fortschritt (%)"].iloc[-1]
budget_status = "75.000€"
budget_diff = "–25.000€"  # Beispiel: Differenz zwischen geplantem und tatsächlichem Budget
risiken = 3  # Beispiel: Anzahl identifizierter Risiken

# Aufteilung der KPI-Anzeige in Spalten
col1, col2, col3 = st.columns(3)
col1.metric("Fortschritt", f"{aktueller_fortschritt:.1f} %", f"{(aktueller_fortschritt - geplanter_fortschritt):+.1f} %")
col2.metric("Budget", budget_status, budget_diff)
col3.metric("Risiken", f"{risiken}", "+1")

# 4. Optional: Tabelle mit Rohdaten anzeigen
st.subheader("Rohdaten – Fortschritt")
st.dataframe(df_progress)
