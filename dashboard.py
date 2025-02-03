import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io

# Setze Seitenkonfiguration
st.set_page_config(layout="wide")

# --- Hilfsfunktion: Data Editor ermitteln (experimental_data_editor oder data_editor) ---
def get_data_editor():
    if hasattr(st, "experimental_data_editor"):
        return st.experimental_data_editor
    elif hasattr(st, "data_editor"):
        return st.data_editor
    else:
        return None

data_editor = get_data_editor()

# Initialisiere Session State für die Performance Metrics (Standardwerte)
if "spm_value" not in st.session_state:
    st.session_state.spm_value = 75
if "spm_ref" not in st.session_state:
    st.session_state.spm_ref = 100  # 100% als Idealwert
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

# Erstelle zwei Tabs: "Dashboard" und "Data Editor"
tabs = st.tabs(["Dashboard", "Data Editor"])

# ===========================
# TAB 1: DASHBOARD
# ===========================
with tabs[0]:
    st.title("Project Performance Dashboard")
    
    st.header("Introduction")
    st.markdown("""
    Project-status reporting is intended to enable decision makers to make informed decisions that will increase the chances of achieving a favorable outcome. Furthermore, it is a vehicle to communicate project performance information to project stakeholders.
    
    The information portrayed in the Project Status Report (PSR) pertains to variances from the original project baseline plans for schedule, cost, quality, and safety.
    
    An effective PSR will command the attention of project executives and decision makers, and help focus their attention on critical deviations from the project’s baseline plans that pose risks to achieving a favorable project outcome.
    
    Unfortunately, PSRs are seldom read by project executives and are often shelved upon issuance.
    
    The underutilization of this project tool is rooted in several factors, including:
    - **Report content:** Common knowledge issues should be discussed in terms of the effectiveness of current mitigation measures while new issues must be clearly identified.
    - **Presentation of project data:** Effective data presentation is key to communicating performance.
    - **Timeliness:** In fast-moving projects, timely reports are crucial to mitigate risks.
    
    This article discusses establishing an effective reporting system to ensure proactive status reporting and executive engagement.
    """)
    
    st.header("Definitions")
    st.markdown("""
    **Schedule Performance Metric (SPM)**  
    Indicator of field progress versus planned progress. Green means on or ahead of schedule; yellow indicates potential delays; red signals significant delays requiring corrective action.
    
    **Cost Contingency Performance Metric (CCPM)**  
    Compares contingency cost drawdown to project progress. Herebei werden die Forecast-Kosten aus der EAC-Tabelle verwendet und der aktuelle (letzte) Actual Cost zugrunde gelegt.
    
    **Safety Performance Metric (SPM)**  
    Compares project safety performance to the industry national average, typically based on OSHA’s Incident Rate (IR).
    
    **Quality Assurance Metric (QAM)**  
    Assesses the contractor’s quality control program, often by comparing non-compliance notices or other quality indicators.
    """)

    # ----------------------
    # Performance Metrics Gauges (aus Session State)
    # ----------------------
    st.header("Performance Metrics Gauges")
    st.markdown("Die folgenden Gauges zeigen die Kennzahlen, die in Tab 2 interaktiv aktualisiert wurden.")
    
    # SPM Gauge
    fig_schedule = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.spm_value,
        delta={'reference': st.session_state.spm_ref, 'increasing': {'color': "red"}},
        title={'text': "Schedule Performance Metric (SPM)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': st.session_state.spm_ref
            }
        }
    ))

    # CCPM Gauge (berechnet aus EAC-Daten)
    fig_cost = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.ccpm_value,
        delta={'reference': st.session_state.ccpm_ref, 'increasing': {'color': "red"}},
        title={'text': "Cost Contingency Performance Metric (CCPM)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': st.session_state.ccpm_ref
            }
        }
    ))

    # Safety SPM Gauge
    fig_safety = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.safety_value,
        delta={'reference': st.session_state.safety_ref, 'increasing': {'color': "red"}},
        title={'text': "Safety Performance Metric (SPM)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 70], 'color': "red"},
                {'range': [70, 90], 'color': "yellow"},
                {'range': [90, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': st.session_state.safety_ref
            }
        }
    ))

    # QAM Gauge
    fig_quality = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=st.session_state.qam_value,
        delta={'reference': st.session_state.qam_ref, 'increasing': {'color': "red"}},
        title={'text': "Quality Assurance Metric (QAM)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 60], 'color': "red"},
                {'range': [60, 85], 'color': "yellow"},
                {'range': [85, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': st.session_state.qam_ref
            }
        }
    ))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_schedule, use_container_width=True)
        st.plotly_chart(fig_cost, use_container_width=True)
    with col2:
        st.plotly_chart(fig_safety, use_container_width=True)
        st.plotly_chart(fig_quality, use_container_width=True)
    
    # ----------------------
    # Additional Diagrams (CFD, BDC, BUC, EAC)
    # ----------------------
    st.header("Additional Diagrams")
    
    # CFD (Cumulative Flow Diagram)
    st.subheader("CFD (Cumulative Flow Diagram)")
    st.markdown("""
    **When Useful:**  
    - Particularly valuable in agile environments or ticket-driven processes to quickly identify bottlenecks.
    - **Tip:** When combined with WIP limits, bottlenecks can be managed more effectively.
    """)
    days = pd.date_range(start="2025-01-01", periods=20)
    backlog = np.random.randint(50, 100, size=20)
    in_progress = np.random.randint(20, 70, size=20)
    done = np.random.randint(10, 50, size=20)
    df_cfd = pd.DataFrame({
        "Date": days,
        "Backlog": backlog,
        "In Progress": in_progress,
        "Done": done
    })
    df_cfd_plot = df_cfd.melt(id_vars=["Date"], value_vars=["Backlog", "In Progress", "Done"],
                              var_name="Stage", value_name="Count")
    fig_cfd = px.area(df_cfd_plot, x="Date", y="Count", color="Stage",
                      title="Cumulative Flow Diagram")
    st.plotly_chart(fig_cfd, use_container_width=True)
    
    # BDC (Burndown Chart)
    st.subheader("BDC (Burndown Chart)")
    st.markdown("""
    **When Useful:**  
    - In time-boxed sprints/iterations to track daily progress.
    - **Tip:** Comparing real versus ideal burndown helps spot deviations.
    """)
    days = pd.date_range(start="2025-02-01", periods=15)
    ideal = np.linspace(100, 0, 15)
    actual = ideal + np.random.normal(0, 5, 15)
    df_bdc = pd.DataFrame({
        "Date": days,
        "Ideal": ideal,
        "Actual": actual
    })
    fig_bdc = go.Figure()
    fig_bdc.add_trace(go.Scatter(x=df_bdc["Date"], y=df_bdc["Ideal"],
                                 mode='lines',
                                 name='Ideal Burndown',
                                 line=dict(dash='dash', color='green')))
    fig_bdc.add_trace(go.Scatter(x=df_bdc["Date"], y=df_bdc["Actual"],
                                 mode='lines+markers',
                                 name='Actual Burndown',
                                 line=dict(color='red')))
    fig_bdc.update_layout(title="Burndown Chart (BDC)",
                          xaxis_title="Date",
                          yaxis_title="Work Remaining (%)")
    st.plotly_chart(fig_bdc, use_container_width=True)
    
    # BUC (Burnup Chart)
    st.subheader("BUC (Burnup Chart)")
    st.markdown("""
    **When Useful:**  
    - When there are frequent scope changes. Shows both progress and scope change.
    - **Tip:** Ideal for status meetings to see “what’s newly added.”
    """)
    days = pd.date_range(start="2025-03-01", periods=15)
    total_scope = np.linspace(100, 130, 15)
    completed = np.linspace(0, 100, 15) + np.random.normal(0, 5, 15)
    df_buc = pd.DataFrame({
        "Date": days,
        "Total Scope": total_scope,
        "Completed": completed
    })
    fig_buc = go.Figure()
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Total Scope"],
                                 mode='lines',
                                 name='Total Scope',
                                 line=dict(color='blue')))
    fig_buc.add_trace(go.Scatter(x=df_buc["Date"], y=df_buc["Completed"],
                                 mode='lines+markers',
                                 name='Completed Work',
                                 line=dict(color='orange')))
    fig_buc.update_layout(title="Burnup Chart (BUC)",
                          xaxis_title="Date",
                          yaxis_title="Work Units")
    st.plotly_chart(fig_buc, use_container_width=True)
    
    # EAC (Estimate at Completion)
    st.subheader("EAC (Estimate at Completion)")
    st.markdown("""
    **When Useful:**  
    - When there are deviations in time or budget.
    - **Tip:** Incorporating EAC into EVM yields a robust cost and performance analysis.
    """)
    days = pd.date_range(start="2025-04-01", periods=15)
    actual_costs = np.linspace(0, 80000, 15) + np.random.normal(0, 2000, 15)
    forecast = actual_costs[-1] + np.linspace(0, 20000, 15)
    df_eac = pd.DataFrame({
        "Date": days,
        "Actual Cost": actual_costs,
        "Forecast Cost": forecast
    })
    fig_eac = go.Figure()
    fig_eac.add_trace(go.Scatter(x=df_eac["Date"], y=df_eac["Actual Cost"],
                                 mode='lines+markers',
                                 name='Actual Cost',
                                 line=dict(color='purple')))
    fig_eac.add_trace(go.Scatter(x=df_eac["Date"], y=df_eac["Forecast Cost"],
                                 mode='lines+markers',
                                 name='Forecast Cost',
                                 line=dict(dash='dash', color='gray')))
    fig_eac.update_layout(title="Estimate at Completion (EAC)",
                          xaxis_title="Date",
                          yaxis_title="Cost (€)")
    st.plotly_chart(fig_eac, use_container_width=True)
    
    st.header("Conclusion")
    st.markdown("""
    In summary, using the PSR as a platform for regular performance presentations led by the project control manager and project executive is an effective method to engage decision makers. Die zusätzlichen Charts und Gauges aktualisieren sich basierend auf den in Tab 2 eingegebenen Daten.
    """)

# ===========================
# TAB 2: DATA EDITOR
# ===========================
with tabs[1]:
    st.title("Manual Data Entry")
    st.markdown("Hier kannst du die zugrunde liegenden Daten bearbeiten. Die eingegebenen Daten fließen in die Berechnung der Kennzahlen ein und aktualisieren die Dashboard-Gauges.")
    
    st.header("Chart Data Editors")
    # CFD Data Editor
    st.subheader("CFD Data")
    sample_cfd = pd.DataFrame({
        "Date": pd.date_range(start="2025-01-01", periods=5).strftime('%Y-%m-%d'),
        "Backlog": [80, 75, 70, 65, 60],
        "In Progress": [30, 35, 40, 45, 50],
        "Done": [10, 15, 20, 25, 30]
    })
    if data_editor is not None:
        edited_cfd = data_editor(sample_cfd, num_rows="dynamic", key="cfd")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_cfd = sample_cfd.to_csv(index=False)
        edited_csv_cfd = st.text_area("Editiere CFD-Daten (CSV)", value=csv_cfd, key="cfd_txt")
        try:
            edited_cfd = pd.read_csv(io.StringIO(edited_csv_cfd))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_cfd = sample_cfd

    # BDC Data Editor
    st.subheader("BDC Data (Burndown Chart)")
    sample_bdc = pd.DataFrame({
        "Date": pd.date_range(start="2025-02-01", periods=5).strftime('%Y-%m-%d'),
        "Ideal": [100, 75, 50, 25, 0],
        "Actual": [105, 80, 55, 30, 5]
    })
    if data_editor is not None:
        edited_bdc = data_editor(sample_bdc, num_rows="dynamic", key="bdc")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_bdc = sample_bdc.to_csv(index=False)
        edited_csv_bdc = st.text_area("Editiere BDC-Daten (CSV)", value=csv_bdc, key="bdc_txt")
        try:
            edited_bdc = pd.read_csv(io.StringIO(edited_csv_bdc))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_bdc = sample_bdc

    # BUC Data Editor
    st.subheader("BUC Data (Burnup Chart)")
    sample_buc = pd.DataFrame({
        "Date": pd.date_range(start="2025-03-01", periods=5).strftime('%Y-%m-%d'),
        "Total Scope": [100, 105, 110, 115, 120],
        "Completed": [0, 20, 40, 60, 80]
    })
    if data_editor is not None:
        edited_buc = data_editor(sample_buc, num_rows="dynamic", key="buc")
    else:
        st.info("Data editor widget nicht verfügbar – bitte aktualisiere Streamlit.")
        csv_buc = sample_buc.to_csv(index=False)
        edited_csv_buc = st.text_area("Editiere BUC-Daten (CSV)", value=csv_buc, key="buc_txt")
        try:
            edited_buc = pd.read_csv(io.StringIO(edited_csv_buc))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_buc = sample_buc

    # EAC Data Editor
    st.subheader("EAC Data (Estimate at Completion)")
    sample_eac = pd.DataFrame({
        "Date": pd.date_range(start="2025-04-01", periods=5).strftime('%Y-%m-%d'),
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
            edited_eac = pd.read_csv(io.StringIO(edited_csv_eac))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_eac = sample_eac

    st.header("Interaktive Kennzahlen-Editoren")
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
            edited_spm = pd.read_csv(io.StringIO(edited_csv_spm))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_spm = sample_spm
    if not edited_spm.empty and edited_spm["Planned Progress"].iloc[0] > 0:
        computed_spm = (edited_spm["Planned Progress"].iloc[0] - edited_spm["Actual Progress"].iloc[0]) / edited_spm["Planned Progress"].iloc[0] * 100
        st.session_state.spm_value = round(computed_spm, 2)
        st.session_state.spm_ref = 100
        st.write(f"Berechnetes SPM: {st.session_state.spm_value:.2f} %")
    
    # Interaktiver CCPM Editor entfällt – CCPM wird aus den EAC-Daten berechnet!
    
    st.header("Additional Data Editors for Safety and Quality")
    # Safety Data Editor
    st.subheader("Safety Data")
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
            edited_safety = pd.read_csv(io.StringIO(edited_csv_safety))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_safety = sample_safety

    # Quality Data Editor
    st.subheader("Quality Data")
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
            edited_quality = pd.read_csv(io.StringIO(edited_csv_quality))
        except Exception as e:
            st.error(f"Fehler beim Parsen: {e}")
            edited_quality = sample_quality

    st.header("Berechnung weiterer Kennzahlen")
    # SPM bereits oben berechnet
    # CCPM aus den EAC-Daten: Verwende den letzten Datensatz
    if not edited_eac.empty:
        last_row = edited_eac.iloc[-1]
        computed_ccpm = (last_row['Actual Cost'] / last_row['Forecast Cost']) * 100
        st.session_state.ccpm_value = round(computed_ccpm, 2)
        st.session_state.ccpm_ref = 100
        st.write(f"Berechnetes CCPM: {st.session_state.ccpm_value:.2f} %")
    
    # Safety SPM aus Safety Data
    if not edited_safety.empty:
        safety_row = edited_safety.iloc[0]
        computed_safety = max(0, (1 - (safety_row['Total Incidents'] / safety_row['Expected Incidents'])) * 100)
        st.session_state.safety_value = round(computed_safety, 2)
        st.session_state.safety_ref = 100
        st.write(f"Berechnetes Safety SPM: {st.session_state.safety_value:.2f} %")
    
    # QAM aus Quality Data
    if not edited_quality.empty:
        quality_row = edited_quality.iloc[0]
        computed_qam = max(0, (1 - (quality_row['NonConformance'] / quality_row['Allowed'])) * 100)
        st.session_state.qam_value = round(computed_qam, 2)
        st.session_state.qam_ref = 100
        st.write(f"Berechnetes QAM: {st.session_state.qam_value:.2f} %")
    
    st.markdown("Die berechneten Kennzahlen werden in den Dashboard-Gauges angezeigt. Beim Wechseln des Tabs oder einem erneuten Ausführen der App werden alle Werte aktualisiert.")
