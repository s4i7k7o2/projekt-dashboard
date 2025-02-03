import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Seitenkonfiguration
st.set_page_config(layout="wide", page_title="GRA Dashboard")

# Hilfsfunktion, um das Datum korrekt zu konvertieren
def convert_date(date_series):
    # Wir erwarten das Format DD.MM.YYYY
    return pd.to_datetime(date_series, format='%d.%m.%Y', dayfirst=True)

# Funktion, um Diagramme für eine Abteilung zu erstellen
def create_sample_diagrams(dept_name, color_scheme):
    st.markdown(f"### {dept_name} – Kennzahlen und Diagramme")
    st.markdown("""
    **Beschreibungen der Diagramme:**
    
    - **CFD (Cumulative Flow Diagram):** Zeigt den kumulierten Arbeitsfortschritt in verschiedenen Phasen (z. B. Backlog, In Progress, Done) über die Zeit. Hilfreich in agilen Umgebungen, um Blockaden zu identifizieren.
    - **BDC (Burndown Chart):** Visualisiert den verbleibenden Arbeitsaufwand innerhalb eines Sprints oder einer Iteration im Vergleich zu einer idealen Abnahme.
    - **BUC (Burnup Chart):** Zeigt den Fortschritt des Projekts sowie Änderungen im Gesamtumfang (Scope) an.
    - **EAC (Estimate at Completion):** Schätzt die Gesamtkosten eines Projekts basierend auf aktuellen Ausgaben und prognostizierten Kosten.
    """)
    
    # CFD Diagramm
    days = pd.date_range(start="2025-01-01", periods=20).strftime('%d.%m.%Y')
    df_cfd = pd.DataFrame({
        "Date": days,
        "Backlog": np.random.randint(50, 100, size=20),
        "In Progress": np.random.randint(20, 70, size=20),
        "Done": np.random.randint(10, 50, size=20)
    })
    # Konvertiere die Datumsspalte in datetime
    df_cfd["Date"] = convert_date(df_cfd["Date"])
    df_cfd_melt = df_cfd.melt(id_vars=["Date"], value_vars=["Backlog", "In Progress", "Done"],
                              var_name="Stage", value_name="Count")
    fig_cfd = px.area(df_cfd_melt, x="Date", y="Count", color="Stage",
                      title=f"{dept_name} – Cumulative Flow Diagram (CFD)")
    fig_cfd.update_xaxes(tickformat="%d.%m.%Y")
    st.plotly_chart(fig_cfd, use_container_width=True)
    
    # BDC Diagramm
    days_bdc = pd.date_range(start="2025-02-01", periods=15).strftime('%d.%m.%Y')
    ideal = np.linspace(100, 0, 15)
    actual = ideal + np.random.normal(0, 5, 15)
    df_bdc = pd.DataFrame({
        "Date": days_bdc,
        "Ideal": ideal,
        "Actual": actual
    })
    df_bdc["Date"] = convert_date(df_bdc["Date"])
    fig_bdc = go.Figure()
    fig_bdc.add_trace(go.Scatter(x=df_bdc["Date"], y=df_bdc["Ideal"],
                                 mode='lines',
                                 name='Ideal Burndown',
                                 line=dict(dash='dash', color='green')))
    fig_bdc.add_trace(go.Scatter(x=df_bdc["Date"], y=df_bdc["Actual"],
                                 mode='lines+markers',
                                 name='Actual Burndown',
                                 line=dict(color='red')))
    fig_bdc.update_layout(title=f"{dept_name} – Burndown Chart (BDC)",
                          xaxis_title="Date",
                          yaxis_title="Work Remaining (%)",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_bdc, use_container_width=True)
    
    # BUC Diagramm
    days_buc = pd.date_range(start="2025-03-01", periods=15).strftime('%d.%m.%Y')
    total_scope = np.linspace(100, 130, 15)
    completed = np.linspace(0, 100, 15) + np.random.normal(0, 5, 15)
    df_buc = pd.DataFrame({
        "Date": days_buc,
        "Total Scope": total_scope,
        "Completed": completed
    })
    df_buc["Date"] = convert_date(df_buc["Date"])
    fig_buc = go.Figure()
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Total Scope"],
                                 mode='lines',
                                 name='Total Scope',
                                 line=dict(color=color_scheme)))
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Completed"],
                                 mode='lines+markers',
                                 name='Completed',
                                 line=dict(color='orange')))
    fig_buc.update_layout(title=f"{dept_name} – Burnup Chart (BUC)",
                          xaxis_title="Date",
                          yaxis_title="Work Units",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_buc, use_container_width=True)
    
    # EAC Diagramm
    days_eac = pd.date_range(start="2025-04-01", periods=15).strftime('%d.%m.%Y')
    actual_costs = np.linspace(0, 80000, 15) + np.random.normal(0, 2000, 15)
    forecast = actual_costs[-1] + np.linspace(0, 20000, 15)
    df_eac = pd.DataFrame({
        "Date": days_eac,
        "Actual Cost": actual_costs,
        "Forecast Cost": forecast
    })
    df_eac["Date"] = convert_date(df_eac["Date"])
    fig_eac = go.Figure()
    fig_eac.add_trace(go.Scatter(x=df_eac["Date"], y=df_eac["Actual Cost"],
                                 mode='lines+markers',
                                 name='Actual Cost',
                                 line=dict(color='purple')))
    fig_eac.add_trace(go.Scatter(x=df_eac["Date"], y=df_eac["Forecast Cost"],
                                 mode='lines+markers',
                                 name='Forecast Cost',
                                 line=dict(dash='dash', color='gray')))
    fig_eac.update_layout(title=f"{dept_name} – Estimate at Completion (EAC)",
                          xaxis_title="Date",
                          yaxis_title="Cost (€)",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_eac, use_container_width=True)

# ===========================
# Data Editor – Gemeinsamer Bereich (Sidebar als Platzhalter)
# ===========================
st.sidebar.title("Data Editor")
st.sidebar.markdown("""
Hier kannst du später gemeinsame Daten bearbeiten, die für alle Abteilungen gelten.
(Dieser Bereich ist momentan ein Platzhalter.)
""")
st.sidebar.write("Platzhalter für Data Editor")

# ===========================
# Tabs für Abteilungsspezifisches Tracking
# ===========================
# Wir verwenden st.tabs, um separate Ansichten für Governance, Risk, Audit & Assessment und Overall GRA zu erzeugen.
dept_tabs = st.tabs(["Governance", "Risk", "Audit & Assessment", "Overall GRA"])

with dept_tabs[0]:
    create_sample_diagrams("Governance", "blue")
with dept_tabs[1]:
    create_sample_diagrams("Risk", "red")
with dept_tabs[2]:
    create_sample_diagrams("Audit & Assessment", "green")
with dept_tabs[3]:
    create_sample_diagrams("Overall GRA", "purple")
