import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io

# Seitenkonfiguration
st.set_page_config(layout="wide", page_title="GRA Dashboard")

# Hilfsfunktion, um den Data Editor zu ermitteln
def get_data_editor():
    if hasattr(st, "experimental_data_editor"):
        return st.experimental_data_editor
    elif hasattr(st, "data_editor"):
        return st.data_editor
    else:
        return None

data_editor = get_data_editor()

# Beispiel: Initialisiere Standardwerte für Kennzahlen in st.session_state (diese können später auch abteilungsspezifisch sein)
if "spm_value" not in st.session_state:
    st.session_state.spm_value = 75
if "spm_ref" not in st.session_state:
    st.session_state.spm_ref = 100
if "ccpm_value" not in st.session_state:
    st.session_state.ccpm_value = 80
if "ccpm_ref" not in st.session_state:
    st.session_state.ccpm_ref = 100
if "safety_value" not in st.session_state:
    st.session_state.safety_value = 60
if "safety_ref" not in st.session_state:
    st.session_state.safety_ref = 100
if "qam_value" not in st.session_state:
    st.session_state.qam_value = 90
if "qam_ref" not in st.session_state:
    st.session_state.qam_ref = 100

# Erstelle Tabs für jede Unterabteilung und eine für die übergeordnete Abteilung
tabs = st.tabs(["Governance", "Risk", "Audit & Assessment", "Overall GRA"])

# -------------------------------
# Beispielhafte Funktion zur Erstellung von Diagrammen
def create_sample_diagrams(dept_name, color_scheme):
    st.markdown(f"### {dept_name} – Kennzahlen und Diagramme")
    st.markdown("""
    **Kurze Beschreibung der Diagramme:**
    
    - **CFD (Cumulative Flow Diagram):** Zeigt den kumulierten Arbeitsfortschritt in verschiedenen Phasen über die Zeit.
    - **BDC (Burndown Chart):** Zeigt den verbleibenden Arbeitsaufwand in einem definierten Zeitraum.
    - **BUC (Burnup Chart):** Visualisiert den Fortschritt sowie eventuelle Scope-Änderungen.
    - **EAC (Estimate at Completion):** Schätzt die Gesamtkosten basierend auf den aktuellen Ausgaben.
    """)
    
    # Erstelle simulierte Daten – auch hier werden die Datumsangaben im Format DD.MM.YYYY erzeugt.
    days = pd.date_range(start="2025-01-01", periods=20).strftime('%d.%m.%Y')
    df = pd.DataFrame({
        "Date": days,
        "Backlog": np.random.randint(50, 100, size=20),
        "In Progress": np.random.randint(20, 70, size=20),
        "Done": np.random.randint(10, 50, size=20)
    })
    df["Date"] = pd.to_datetime(df["Date"], format='%d.%m.%Y', dayfirst=True)
    df_melt = df.melt(id_vars=["Date"], value_vars=["Backlog", "In Progress", "Done"],
                      var_name="Stage", value_name="Count")
    fig_cfd = px.area(df_melt, x="Date", y="Count", color="Stage",
                      title=f"{dept_name} – Cumulative Flow Diagram")
    fig_cfd.update_xaxes(tickformat="%d.%m.%Y")
    
    st.plotly_chart(fig_cfd, use_container_width=True)
    
    # Beispiel: Burndown Chart
    days_bdc = pd.date_range(start="2025-02-01", periods=15).strftime('%d.%m.%Y')
    ideal = np.linspace(100, 0, 15)
    actual = ideal + np.random.normal(0, 5, 15)
    df_bdc = pd.DataFrame({
        "Date": days_bdc,
        "Ideal": ideal,
        "Actual": actual
    })
    df_bdc["Date"] = pd.to_datetime(df_bdc["Date"], format='%d.%m.%Y', dayfirst=True)
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
    
    # Burnup Chart
    days_buc = pd.date_range(start="2025-03-01", periods=15).strftime('%d.%m.%Y')
    total_scope = np.linspace(100, 130, 15)
    completed = np.linspace(0, 100, 15) + np.random.normal(0, 5, 15)
    df_buc = pd.DataFrame({
        "Date": days_buc,
        "Total Scope": total_scope,
        "Completed": completed
    })
    df_buc["Date"] = pd.to_datetime(df_buc["Date"], format='%d.%m.%Y', dayfirst=True)
    fig_buc = go.Figure()
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Total Scope"],
                                 mode='lines',
                                 name='Total Scope',
                                 line=dict(color=color_scheme)))
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Completed"],
                                 mode='lines+markers',
                                 name='Completed Work',
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
    df_eac["Date"] = pd.to_datetime(df_eac["Date"], format='%d.%m.%Y', dayfirst=True)
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

# -------------------------------
# TAB 2: DATA EDITOR – Gemeinsame Bearbeitung der Daten
# -------------------------------
with tabs[1]:
    st.title("Data Editor – GRA Tracking")
    st.markdown("""
    Hier kannst du die zugrunde liegenden Daten bearbeiten. 
    Die Eingaben fließen in die Berechnung der Kennzahlen ein und aktualisieren die Diagramme in den einzelnen Abteilungs-Tabs.
    """)
    
    st.header("Interaktive Kennzahlen-Editoren")
    st.markdown("Bearbeite die folgenden Tabellen. Die Kennzahlen werden automatisch anhand der Eingaben berechnet.")
    
    # Interaktiver SPM Editor (Planned Progress und Actual Progress)
    st.subheader("Interaktiver SPM Editor")
    sample_spm = pd.DataFrame({
        "Planned Progress": [100],
        "Actual Progress": [85]
    })
    if data_editor is not None:
        edited_spm = data_editor(sample_spm, num_rows="static", key="spm_editor")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_spm = sample_spm.to_csv(index=False)
        edited_csv_spm = st.text_area("Editiere SPM-Daten (CSV)", value=csv_spm, key="spm_txt")
        try:
            edited_spm = pd.read_csv(io.StringIO(edited_csv_spm), sep=",")
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_spm = sample_spm
    if not edited_spm.empty and edited_spm["Planned Progress"].iloc[0] > 0:
        computed_spm = (edited_spm["Planned Progress"].iloc[0] - edited_spm["Actual Progress"].iloc[0]) / edited_spm["Planned Progress"].iloc[0] * 100
        st.session_state.spm_value = round(computed_spm, 2)
        st.session_state.spm_ref = 100
        st.write(f"Berechnetes SPM: {st.session_state.spm_value:.2f} %")
    
    # EAC Data Editor (wird auch zur Berechnung von CCPM genutzt)
    st.subheader("EAC Data Editor")
    sample_eac = pd.DataFrame({
        "Date": pd.date_range(start="2025-04-01", periods=5).strftime('%d.%m.%Y'),
        "Actual Cost": [0, 10000, 20000, 30000, 40000],
        "Forecast Cost": [50000, 50000, 50000, 50000, 50000]
    })
    if data_editor is not None:
        edited_eac = data_editor(sample_eac, num_rows="dynamic", key="eac")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_eac = sample_eac.to_csv(index=False)
        edited_csv_eac = st.text_area("Editiere EAC-Daten (CSV)", value=csv_eac, key="eac_txt")
        try:
            edited_eac = pd.read_csv(io.StringIO(edited_csv_eac), sep=",")
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_eac = sample_eac
    # Berechne CCPM basierend auf dem letzten Datensatz der EAC-Tabelle
    if not edited_eac.empty:
        last_row = edited_eac.iloc[-1]
        computed_ccpm = (last_row['Actual Cost'] / last_row['Forecast Cost']) * 100
        st.session_state.ccpm_value = round(computed_ccpm, 2)
        st.session_state.ccpm_ref = 100
        st.write(f"Berechnetes CCPM: {st.session_state.ccpm_value:.2f} %")
    
    # Safety Data Editor
    st.subheader("Safety Data Editor")
    sample_safety = pd.DataFrame({
        "Total Incidents": [2],
        "Expected Incidents": [5]
    })
    if data_editor is not None:
        edited_safety = data_editor(sample_safety, num_rows="static", key="safety")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_safety = sample_safety.to_csv(index=False)
        edited_csv_safety = st.text_area("Editiere Safety-Daten (CSV)", value=csv_safety, key="safety_txt")
        try:
            edited_safety = pd.read_csv(io.StringIO(edited_csv_safety), sep=",")
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_safety = sample_safety

    # Quality Data Editor
    st.subheader("Quality Data Editor")
    sample_quality = pd.DataFrame({
        "NonConformance": [1],
        "Allowed": [10]
    })
    if data_editor is not None:
        edited_quality = data_editor(sample_quality, num_rows="static", key="quality")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_quality = sample_quality.to_csv(index=False)
        edited_csv_quality = st.text_area("Editiere Quality-Daten (CSV)", value=csv_quality, key="quality_txt")
        try:
            edited_quality = pd.read_csv(io.StringIO(edited_csv_quality), sep=",")
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_quality = sample_quality

    # Safety SPM und QAM Berechnungen
    if not edited_safety.empty:
        safety_row = edited_safety.iloc[0]
        computed_safety = max(0, (1 - (safety_row['Total Incidents'] / safety_row['Expected Incidents'])) * 100)
        st.session_state.safety_value = round(computed_safety, 2)
        st.session_state.safety_ref = 100
        st.write(f"Berechnetes Safety SPM: {st.session_state.safety_value:.2f} %")
    
    if not edited_quality.empty:
        quality_row = edited_quality.iloc[0]
        computed_qam = max(0, (1 - (quality_row['NonConformance'] / quality_row['Allowed'])) * 100)
        st.session_state.qam_value = round(computed_qam, 2)
        st.session_state.qam_ref = 100
        st.write(f"Berechnetes QAM: {st.session_state.qam_value:.2f} %")
    
    st.markdown("Die berechneten Kennzahlen werden in den Dashboard-Gauges angezeigt. Beim Wechseln des Tabs oder einem erneuten Ausführen der App werden alle Werte aktualisiert.")
