import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io

# Seitenkonfiguration
st.set_page_config(layout="wide", page_title="GRA Dashboard")

# -------------------------------
# Hilfsfunktionen
# -------------------------------
def get_data_editor():
    if hasattr(st, "experimental_data_editor"):
        return st.experimental_data_editor
    elif hasattr(st, "data_editor"):
        return st.data_editor
    else:
        return None

data_editor = get_data_editor()

def convert_date(date_series):
    # Erwartet das Format DD.MM.YYYY und konvertiert in datetime
    return pd.to_datetime(date_series, format='%d.%m.%Y', dayfirst=True)

# -------------------------------
# Default-Daten für jede Unterabteilung
# -------------------------------
def default_cfd():
    dates = pd.date_range(start="2025-01-01", periods=5).strftime('%d.%m.%Y')
    return pd.DataFrame({
        "Date": dates,
        "Backlog": [80, 75, 70, 65, 60],
        "In Progress": [30, 35, 40, 45, 50],
        "Done": [10, 15, 20, 25, 30]
    })

def default_bdc():
    dates = pd.date_range(start="2025-02-01", periods=5).strftime('%d.%m.%Y')
    return pd.DataFrame({
        "Date": dates,
        "Ideal": [100, 75, 50, 25, 0],
        "Actual": [105, 80, 55, 30, 5]
    })

def default_buc():
    dates = pd.date_range(start="2025-03-01", periods=5).strftime('%d.%m.%Y')
    return pd.DataFrame({
        "Date": dates,
        "Total Scope": [100, 105, 110, 115, 120],
        "Completed": [0, 20, 40, 60, 80]
    })

# Für den EAC (nur Overall)
def default_eac():
    dates = pd.date_range(start="2025-04-01", periods=5).strftime('%d.%m.%Y')
    return pd.DataFrame({
        "Date": dates,
        "Actual Cost": [0, 10000, 20000, 30000, 40000],
        "Forecast Cost": [50000, 50000, 50000, 50000, 50000]
    })

# -------------------------------
# Initialisiere Session State – falls nicht vorhanden
# Für jede Unterabteilung speichern wir CFD, BDC, BUC
for dept in ["Gov", "Risk", "Audit"]:
    if f"{dept}_CFD" not in st.session_state:
        st.session_state[f"{dept}_CFD"] = default_cfd()
    if f"{dept}_BDC" not in st.session_state:
        st.session_state[f"{dept}_BDC"] = default_bdc()
    if f"{dept}_BUC" not in st.session_state:
        st.session_state[f"{dept}_BUC"] = default_buc()

# EAC-Daten (Overall)
if "EAC" not in st.session_state:
    st.session_state["EAC"] = default_eac()

# Für die Kennzahlen (SPM, CCPM, Safety, QAM)
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

# -------------------------------
# Dashboard Tab (Hauptinhalt)
# -------------------------------
tabs = st.tabs(["Dashboard", "Data Editor"])

with tabs[0]:
    st.title("Project Performance Dashboard")
    st.header("Introduction")
    st.markdown("""
    Project-status reporting is intended to enable decision makers to make informed decisions that will increase the chances of achieving a favorable outcome. Furthermore, it is a vehicle to communicate project performance information to project stakeholders.
    
    ... [Weitere Einleitungstexte] ...
    """)
    
    st.header("Definitions")
    st.markdown("""
    **Schedule Performance Metric (SPM):** Fortschrittsvergleich, etc.  
    **Cost Contingency Performance Metric (CCPM):** Vergleicht aktuelle Kosten mit Forecast.  
    **Safety Performance Metric (SPM):** Basierend auf Incident Rate.  
    **Quality Assurance Metric (QAM):** Qualitätskontrolle.
    """)
    
    st.header("Performance Metrics Gauges")
    # Hier werden die Gauges angezeigt (Werte aus st.session_state)
    fig_spm = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.spm_value,
        delta={'reference': st.session_state.spm_ref, 'increasing': {'color': "red"}},
        title={'text': "SPM"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    fig_ccpm = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.ccpm_value,
        delta={'reference': st.session_state.ccpm_ref, 'increasing': {'color': "red"}},
        title={'text': "CCPM"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    fig_safety = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.safety_value,
        delta={'reference': st.session_state.safety_ref, 'increasing': {'color': "red"}},
        title={'text': "Safety SPM"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    fig_qam = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.qam_value,
        delta={'reference': st.session_state.qam_ref, 'increasing': {'color': "red"}},
        title={'text': "QAM"},
        gauge={'axis': {'range': [0, 100]}}
    ))
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_spm, use_container_width=True)
        st.plotly_chart(fig_ccpm, use_container_width=True)
    with col2:
        st.plotly_chart(fig_safety, use_container_width=True)
        st.plotly_chart(fig_qam, use_container_width=True)
    
    st.header("Additional Diagrams")
    st.markdown("""
    **CFD:** Kumulativer Flow, **BDC:** Burndown Chart, **BUC:** Burnup Chart, **EAC:** Estimate at Completion (nur im Overall-Tab)
    """)
    # Hier werden im Dashboard die Diagramme aus dem Data Editor angezeigt.
    # Beispiel: CFD
    df_cfd_overall = st.session_state["Gov_CFD"].copy()  # für Demo: verwende Governance-Daten
    df_cfd_overall["Date"] = convert_date(df_cfd_overall["Date"])
    df_cfd_melt = df_cfd_overall.melt(id_vars=["Date"], value_vars=["Backlog", "In Progress", "Done"],
                                      var_name="Stage", value_name="Count")
    fig_cfd_overall = px.area(df_cfd_melt, x="Date", y="Count", color="Stage",
                              title="Overall CFD (Beispiel: Governance-Daten)")
    fig_cfd_overall.update_xaxes(tickformat="%d.%m.%Y")
    st.plotly_chart(fig_cfd_overall, use_container_width=True)
    
    st.markdown("Weitere Diagramme (BDC, BUC) werden in den Abteilungstabs angezeigt.")

# -------------------------------
# Data Editor Tab – Bearbeitbare Daten (Sidebar nicht verschachtelt)
# -------------------------------
with tabs[1]:
    st.title("Data Editor – GRA Tracking")
    st.markdown("Hier kannst du die zugrunde liegenden Daten bearbeiten. Die Änderungen wirken sich beim nächsten Rerun (z. B. nach Tab-Wechsel) in den Diagrammen aus.")
    
    # Für jede Unterabteilung separat
    for dept, name in zip(["Gov", "Risk", "Audit"], ["Governance", "Risk", "Audit & Assessment"]):
        st.subheader(f"{name} – CFD Daten")
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept}_CFD"], num_rows="dynamic", key=f"{dept}_CFD_editor")
        else:
            csv_text = st.text_area(f"CFD {name} (CSV)", value=st.session_state[f"{dept}_CFD"].to_csv(index=False), key=f"{dept}_CFD_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited = st.session_state[f"{dept}_CFD"]
        st.session_state[f"{dept}_CFD"] = edited

        st.subheader(f"{name} – BDC Daten")
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept}_BDC"], num_rows="dynamic", key=f"{dept}_BDC_editor")
        else:
            csv_text = st.text_area(f"BDC {name} (CSV)", value=st.session_state[f"{dept}_BDC"].to_csv(index=False), key=f"{dept}_BDC_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited = st.session_state[f"{dept}_BDC"]
        st.session_state[f"{dept}_BDC"] = edited

        st.subheader(f"{name} – BUC Daten")
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept}_BUC"], num_rows="dynamic", key=f"{dept}_BUC_editor")
        else:
            csv_text = st.text_area(f"BUC {name} (CSV)", value=st.session_state[f"{dept}_BUC"].to_csv(index=False), key=f"{dept}_BUC_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited = st.session_state[f"{dept}_BUC"]
        st.session_state[f"{dept}_BUC"] = edited

    # EAC Daten (Overall)
    st.subheader("EAC Daten (Overall)")
    if data_editor is not None:
        edited = data_editor(st.session_state["EAC"], num_rows="dynamic", key="EAC_editor")
    else:
        csv_text = st.text_area("EAC Daten (CSV)", value=st.session_state["EAC"].to_csv(index=False), key="EAC_csv")
        try:
            edited = pd.read_csv(io.StringIO(csv_text), sep=",")
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited = st.session_state["EAC"]
    st.session_state["EAC"] = edited

    st.header("Interaktive Kennzahlen-Editoren")
    st.subheader("Interaktiver SPM Editor")
    sample_spm = pd.DataFrame({
        "Planned Progress": [100],
        "Actual Progress": [85]
    })
    if data_editor is not None:
        edited_spm = data_editor(sample_spm, num_rows="static", key="spm_editor")
    else:
        csv_text = st.text_area("SPM Daten (CSV)", value=sample_spm.to_csv(index=False), key="spm_csv")
        try:
            edited_spm = pd.read_csv(io.StringIO(csv_text), sep=",")
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_spm = sample_spm
    if not edited_spm.empty and edited_spm["Planned Progress"].iloc[0] > 0:
        computed_spm = (edited_spm["Planned Progress"].iloc[0] - edited_spm["Actual Progress"].iloc[0]) / edited_spm["Planned Progress"].iloc[0] * 100
        st.session_state.spm_value = round(computed_spm, 2)
        st.session_state.spm_ref = 100
        st.write(f"Berechnetes SPM: {st.session_state.spm_value:.2f} %")
    
    st.header("Safety und Quality Daten")
    with st.expander("Safety Daten"):
        sample_safety = pd.DataFrame({"Total Incidents": [2], "Expected Incidents": [5]})
        if data_editor is not None:
            edited_safety = data_editor(sample_safety, num_rows="static", key="safety_editor")
        else:
            csv_text = st.text_area("Safety Daten (CSV)", value=sample_safety.to_csv(index=False), key="safety_csv")
            try:
                edited_safety = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited_safety = sample_safety
        st.session_state["Safety"] = edited_safety
    with st.expander("Quality Daten"):
        sample_quality = pd.DataFrame({"NonConformance": [1], "Allowed": [10]})
        if data_editor is not None:
            edited_quality = data_editor(sample_quality, num_rows="static", key="quality_editor")
        else:
            csv_text = st.text_area("Quality Daten (CSV)", value=sample_quality.to_csv(index=False), key="quality_csv")
            try:
                edited_quality = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited_quality = sample_quality
        st.session_state["Quality"] = edited_quality

    st.header("Berechnung weiterer Kennzahlen")
    # CCPM aus EAC-Daten
    if not st.session_state["EAC"].empty:
        last_row = st.session_state["EAC"].iloc[-1]
        computed_ccpm = (last_row["Actual Cost"] / last_row["Forecast Cost"]) * 100
        st.session_state.ccpm_value = round(computed_ccpm, 2)
        st.session_state.ccpm_ref = 100
        st.write(f"Berechnetes CCPM: {st.session_state.ccpm_value:.2f} %")
    # Safety SPM
    safety_row = st.session_state["Safety"].iloc[0]
    computed_safety = max(0, (1 - (safety_row["Total Incidents"] / safety_row["Expected Incidents"])) * 100)
    st.session_state.safety_value = round(computed_safety, 2)
    st.session_state.safety_ref = 100
    st.write(f"Berechnetes Safety SPM: {st.session_state.safety_value:.2f} %")
    # QAM
    quality_row = st.session_state["Quality"].iloc[0]
    computed_qam = max(0, (1 - (quality_row["NonConformance"] / quality_row["Allowed"])) * 100)
    st.session_state.qam_value = round(computed_qam, 2)
    st.session_state.qam_ref = 100
    st.write(f"Berechnetes QAM: {st.session_state.qam_value:.2f} %")
    
    st.markdown("Die bearbeiteten Daten und berechneten Kennzahlen werden in den Abteilungstabs angezeigt (beim Wechseln des Tabs oder bei erneutem Ausführen der App).")
    
# -------------------------------
# Abteilungstabs: Governance, Risk, Audit & Assessment, Overall GRA
# -------------------------------
dept_tabs = st.tabs(["Governance", "Risk", "Audit & Assessment", "Overall GRA"])

def render_dept_tab(dept_key, dept_name, color_scheme):
    st.markdown(f"### {dept_name} – Kennzahlen und Diagramme")
    # CFD
    df_cfd = st.session_state[f"{dept_key}_CFD"].copy()
    df_cfd["Date"] = convert_date(df_cfd["Date"])
    df_cfd_melt = df_cfd.melt(id_vars=["Date"], value_vars=["Backlog", "In Progress", "Done"],
                               var_name="Stage", value_name="Count")
    fig_cfd = px.area(df_cfd_melt, x="Date", y="Count", color="Stage",
                      title=f"{dept_name} – Cumulative Flow Diagram (CFD)")
    fig_cfd.update_xaxes(tickformat="%d.%m.%Y")
    st.plotly_chart(fig_cfd, use_container_width=True)
    
    # BDC
    df_bdc = st.session_state[f"{dept_key}_BDC"].copy()
    df_bdc["Date"] = convert_date(df_bdc["Date"])
    fig_bdc = go.Figure()
    fig_bdc.add_trace(go.Scatter(x=df_bdc["Date"], y=df_bdc["Ideal"],
                                 mode='lines', name='Ideal Burndown',
                                 line=dict(dash='dash', color='green')))
    fig_bdc.add_trace(go.Scatter(x=df_bdc["Date"], y=df_bdc["Actual"],
                                 mode='lines+markers', name='Actual Burndown',
                                 line=dict(color='red')))
    fig_bdc.update_layout(title=f"{dept_name} – Burndown Chart (BDC)",
                          xaxis_title="Date", yaxis_title="Work Remaining (%)",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_bdc, use_container_width=True)
    
    # BUC
    df_buc = st.session_state[f"{dept_key}_BUC"].copy()
    df_buc["Date"] = convert_date(df_buc["Date"])
    fig_buc = go.Figure()
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Total Scope"],
                                 mode='lines', name='Total Scope',
                                 line=dict(color=color_scheme)))
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Completed"],
                                 mode='lines+markers', name='Completed',
                                 line=dict(color='orange')))
    fig_buc.update_layout(title=f"{dept_name} – Burnup Chart (BUC)",
                          xaxis_title="Date", yaxis_title="Work Units",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_buc, use_container_width=True)

with dept_tabs[0]:
    render_dept_tab("Gov", "Governance", "blue")
with dept_tabs[1]:
    render_dept_tab("Risk", "Risk", "red")
with dept_tabs[2]:
    render_dept_tab("Audit", "Audit & Assessment", "green")
with dept_tabs[3]:
    st.markdown("### Overall GRA – Aggregierte Kennzahlen und Diagramme")
    # Aggregiere CFD
    dfs_cfd = []
    for dept in ["Gov", "Risk", "Audit"]:
        df = st.session_state[f"{dept}_CFD"].copy()
        df["Date"] = convert_date(df["Date"])
        dfs_cfd.append(df)
    df_overall_cfd = dfs_cfd[0].copy()
    for col in ["Backlog", "In Progress", "Done"]:
        df_overall_cfd[col] = sum(df[col] for df in dfs_cfd)
    df_overall_cfd_melt = df_overall_cfd.melt(id_vars=["Date"], value_vars=["Backlog", "In Progress", "Done"],
                                              var_name="Stage", value_name="Count")
    fig_overall_cfd = px.area(df_overall_cfd_melt, x="Date", y="Count", color="Stage",
                              title="Overall GRA – Cumulative Flow Diagram (CFD)")
    fig_overall_cfd.update_xaxes(tickformat="%d.%m.%Y")
    st.plotly_chart(fig_overall_cfd, use_container_width=True)
    
    # Aggregiere BDC
    dfs_bdc = []
    for dept in ["Gov", "Risk", "Audit"]:
        df = st.session_state[f"{dept}_BDC"].copy()
        df["Date"] = convert_date(df["Date"])
        dfs_bdc.append(df)
    df_overall_bdc = dfs_bdc[0].copy()
    for col in ["Ideal", "Actual"]:
        df_overall_bdc[col] = sum(df[col] for df in dfs_bdc)
    fig_overall_bdc = go.Figure()
    fig_overall_bdc.add_trace(go.Scatter(x=df_overall_bdc["Date"], y=df_overall_bdc["Ideal"],
                                         mode='lines',
                                         name='Ideal Burndown',
                                         line=dict(dash='dash', color='green')))
    fig_overall_bdc.add_trace(go.Scatter(x=df_overall_bdc["Date"], y=df_overall_bdc["Actual"],
                                         mode='lines+markers',
                                         name='Actual Burndown',
                                         line=dict(color='red')))
    fig_overall_bdc.update_layout(title="Overall GRA – Burndown Chart (BDC)",
                                  xaxis_title="Date",
                                  yaxis_title="Work Remaining (%)",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_bdc, use_container_width=True)
    
    # Aggregiere BUC
    dfs_buc = []
    for dept in ["Gov", "Risk", "Audit"]:
        df = st.session_state[f"{dept}_BUC"].copy()
        df["Date"] = convert_date(df["Date"])
        dfs_buc.append(df)
    df_overall_buc = dfs_buc[0].copy()
    for col in ["Total Scope", "Completed"]:
        df_overall_buc[col] = sum(df[col] for df in dfs_buc)
    fig_overall_buc = go.Figure()
    fig_overall_buc.add_trace(go.Scatter(x=df_overall_buc["Date"], y=df_overall_buc["Total Scope"],
                                         mode='lines',
                                         name='Total Scope',
                                         line=dict(color='purple')))
    fig_overall_buc.add_trace(go.Scatter(x=df_overall_buc["Date"], y=df_overall_buc["Completed"],
                                         mode='lines+markers',
                                         name='Completed',
                                         line=dict(color='orange')))
    fig_overall_buc.update_layout(title="Overall GRA – Burnup Chart (BUC)",
                                  xaxis_title="Date",
                                  yaxis_title="Work Units",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_buc, use_container_width=True)
    
    # EAC Diagramm nur im Overall Tab
    df_overall_eac = st.session_state["EAC"].copy()
    df_overall_eac["Date"] = convert_date(df_overall_eac["Date"])
    fig_overall_eac = go.Figure()
    fig_overall_eac.add_trace(go.Scatter(x=df_overall_eac["Date"], y=df_overall_eac["Actual Cost"],
                                         mode='lines+markers',
                                         name='Actual Cost',
                                         line=dict(color='brown')))
    fig_overall_eac.add_trace(go.Scatter(x=df_overall_eac["Date"], y=df_overall_eac["Forecast Cost"],
                                         mode='lines+markers',
                                         name='Forecast Cost',
                                         line=dict(dash='dash', color='gray')))
    fig_overall_eac.update_layout(title="Overall GRA – Estimate at Completion (EAC)",
                                  xaxis_title="Date",
                                  yaxis_title="Cost (€)",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_eac, use_container_width=True)
    
    st.markdown("### Conclusion")
    st.markdown("""
    Die aggregierten Daten der Unterabteilungen werden hier zusammengeführt.
    Änderungen im Data Editor (Sidebar) wirken sich beim nächsten Rerun/Tabwechsel auf die Diagramme in den Abteilungstabs und der Overall-Ansicht aus.
    """)
