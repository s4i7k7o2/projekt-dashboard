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
# Default-Daten für die Diagramme
# -------------------------------
def default_cfd():
    dates = pd.date_range(start="2025-01-02", periods=20).strftime('%d.%m.%Y')
    return pd.DataFrame({
        "Date": dates,
        "Backlog": np.random.randint(50, 100, size=20),
        "In Progress": np.random.randint(20, 70, size=20),
        "Done": np.random.randint(10, 50, size=20)
    })

def default_bdc():
    dates = pd.date_range(start="2025-02-01", periods=15).strftime('%d.%m.%Y')
    ideal = np.linspace(100, 0, 15)
    actual = ideal + np.random.normal(0, 5, 15)
    return pd.DataFrame({
        "Date": dates,
        "Ideal": ideal,
        "Actual": actual
    })

def default_buc():
    dates = pd.date_range(start="2025-03-01", periods=15).strftime('%d.%m.%Y')
    total_scope = np.linspace(100, 130, 15)
    completed = np.linspace(0, 100, 15) + np.random.normal(0, 5, 15)
    return pd.DataFrame({
        "Date": dates,
        "Total Scope": total_scope,
        "Completed": completed
    })

def default_eac():
    dates = pd.date_range(start="2025-04-01", periods=15).strftime('%d.%m.%Y')
    actual_costs = np.linspace(0, 80000, 15) + np.random.normal(0, 2000, 15)
    forecast = actual_costs[-1] + np.linspace(0, 20000, 15)
    return pd.DataFrame({
        "Date": dates,
        "Actual Cost": actual_costs,
        "Forecast Cost": forecast
    })

# -------------------------------
# Session State initialisieren
# -------------------------------
for dept in ["Gov", "Risk", "Audit"]:
    if f"{dept}_CFD" not in st.session_state:
        st.session_state[f"{dept}_CFD"] = default_cfd()
    if f"{dept}_BDC" not in st.session_state:
        st.session_state[f"{dept}_BDC"] = default_bdc()
    if f"{dept}_BUC" not in st.session_state:
        st.session_state[f"{dept}_BUC"] = default_buc()

if "EAC" not in st.session_state:
    st.session_state["EAC"] = default_eac()

# Beispiel-Basiswerte für Kennzahlen
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
# Sidebar: Abteilungsauswahl und Data Editor
# -------------------------------
selected_dept = st.sidebar.selectbox(
    "Wähle eine Abteilung:",
    options=["GRA-Overall", "Governance", "Risk", "Audit & Assessment"]
)

if selected_dept == "GRA-Overall":
    st.sidebar.markdown("### Data Editor für Overall – EAC Daten")
    with st.sidebar.expander("EAC Daten bearbeiten"):
        if data_editor is not None:
            edited_eac = data_editor(st.session_state["EAC"], num_rows="dynamic", key="EAC_editor")
        else:
            csv_text = st.text_area("EAC Daten (CSV)", value=st.session_state["EAC"].to_csv(index=False), key="EAC_csv")
            try:
                edited_eac = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited_eac = st.session_state["EAC"]
        st.session_state["EAC"] = edited_eac
else:
    dept_key = {"Governance": "Gov", "Risk": "Risk", "Audit & Assessment": "Audit"}[selected_dept]
    st.sidebar.markdown(f"### Data Editor für {selected_dept}")
    with st.sidebar.expander(f"{selected_dept} – CFD Daten"):
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept_key}_CFD"], num_rows="dynamic", key=f"{dept_key}_CFD_editor")
        else:
            csv_text = st.text_area(f"CFD {selected_dept} (CSV)", value=st.session_state[f"{dept_key}_CFD"].to_csv(index=False), key=f"{dept_key}_CFD_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited = st.session_state[f"{dept_key}_CFD"]
        st.session_state[f"{dept_key}_CFD"] = edited

    with st.sidebar.expander(f"{selected_dept} – BDC Daten"):
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept_key}_BDC"], num_rows="dynamic", key=f"{dept_key}_BDC_editor")
        else:
            csv_text = st.text_area(f"BDC {selected_dept} (CSV)", value=st.session_state[f"{dept_key}_BDC"].to_csv(index=False), key=f"{dept_key}_BDC_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited = st.session_state[f"{dept_key}_BDC"]
        st.session_state[f"{dept_key}_BDC"] = edited

    with st.sidebar.expander(f"{selected_dept} – BUC Daten"):
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept_key}_BUC"], num_rows="dynamic", key=f"{dept_key}_BUC_editor")
        else:
            csv_text = st.text_area(f"BUC {selected_dept} (CSV)", value=st.session_state[f"{dept_key}_BUC"].to_csv(index=False), key=f"{dept_key}_BUC_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Fehler beim Parsen: {e}")
                edited = st.session_state[f"{dept_key}_BUC"]
        st.session_state[f"{dept_key}_BUC"] = edited

# -------------------------------
# Main-Bereich: Darstellung der Diagramme
# -------------------------------
st.title(f"{selected_dept} Dashboard")

def render_charts_for_dept(dept_key, dept_name, color_scheme):
    st.markdown(f"### {dept_name} – Kennzahlen und Diagramme")
    # CFD: Gestapelte Darstellung als Stacked Area Chart mit line_shape 'linear' (ZickZag)
    df_cfd = st.session_state[f"{dept_key}_CFD"].copy()
    df_cfd["Date"] = convert_date(df_cfd["Date"])
    df_cfd = df_cfd.sort_values("Date")
    fig_cfd = go.Figure()
    # Verwende line_shape 'linear', um direkt von Punkt zu Punkt zu verbinden (so entsteht ein zickzackartiger Verlauf)
    for stage, col, trace_color in zip(["Backlog", "In Progress", "Done"],
                                       ["Backlog", "In Progress", "Done"],
                                       ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        fig_cfd.add_trace(go.Scatter(
            x=df_cfd["Date"],
            y=df_cfd[col],
            mode="lines",
            name=stage,
            stackgroup="one",
            line=dict(color=trace_color, width=2, shape="linear"),
            hovertemplate='%{x|%d.%m.%Y}<br>' + stage + ': %{y}<extra></extra>'
        ))
    fig_cfd.update_layout(title=f"{dept_name} – Cumulative Flow Diagram (CFD)",
                          xaxis_title="Date", yaxis_title="Count",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_cfd, use_container_width=True)
    
    # BDC Diagramm
    df_bdc = st.session_state[f"{dept_key}_BDC"].copy()
    df_bdc["Date"] = convert_date(df_bdc["Date"])
    df_bdc = df_bdc.sort_values("Date")
    fig_bdc = go.Figure()
    fig_bdc.add_trace(go.Scatter(
        x=df_bdc["Date"], y=df_bdc["Ideal"],
        mode='lines', name='Ideal Burndown',
        line=dict(dash='dash', color='green'),
        hovertemplate='%{x|%d.%m.%Y}<br>Ideal: %{y}<extra></extra>'
    ))
    fig_bdc.add_trace(go.Scatter(
        x=df_bdc["Date"], y=df_bdc["Actual"],
        mode='lines+markers', name='Actual Burndown',
        line=dict(color='red'),
        hovertemplate='%{x|%d.%m.%Y}<br>Actual: %{y}<extra></extra>'
    ))
    fig_bdc.update_layout(title=f"{dept_name} – Burndown Chart (BDC)",
                          xaxis_title="Date", yaxis_title="Work Remaining (%)",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_bdc, use_container_width=True)
    
    # BUC Diagramm
    df_buc = st.session_state[f"{dept_key}_BUC"].copy()
    df_buc["Date"] = convert_date(df_buc["Date"])
    df_buc = df_buc.sort_values("Date")
    fig_buc = go.Figure()
    fig_buc.add_trace(go.Scatter(
        x=df_buc["Date"], y=df_buc["Total Scope"],
        mode='lines', name='Total Scope',
        line=dict(color=color_scheme),
        hovertemplate='%{x|%d.%m.%Y}<br>Total Scope: %{y}<extra></extra>'
    ))
    fig_buc.add_trace(go.Scatter(
        x=df_buc["Date"], y=df_buc["Completed"],
        mode='lines+markers', name='Completed',
        line=dict(color='orange'),
        hovertemplate='%{x|%d.%m.%Y}<br>Completed: %{y}<extra></extra>'
    ))
    fig_buc.update_layout(title=f"{dept_name} – Burnup Chart (BUC)",
                          xaxis_title="Date", yaxis_title="Work Units",
                          xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_buc, use_container_width=True)

# Render-Diagramme je nach Auswahl in der Sidebar
if selected_dept == "GRA-Overall":
    st.markdown("### Overall GRA – Aggregierte Kennzahlen und Diagramme")
    # Aggregiere CFD-Daten aus allen drei Unterabteilungen
    dfs_cfd = []
    for dept in ["Gov", "Risk", "Audit"]:
        df = st.session_state[f"{dept}_CFD"].copy()
        df["Date"] = convert_date(df["Date"])
        dfs_cfd.append(df)
    df_overall_cfd = pd.concat(dfs_cfd).groupby("Date", as_index=False).sum()
    fig_overall_cfd = go.Figure()
    for stage, col, trace_color in zip(["Backlog", "In Progress", "Done"],
                                       ["Backlog", "In Progress", "Done"],
                                       ["#1f77b4", "#ff7f0e", "#2ca02c"]):
        fig_overall_cfd.add_trace(go.Scatter(
            x=df_overall_cfd["Date"],
            y=df_overall_cfd[col],
            mode="lines",
            name=stage,
            stackgroup="one",
            line=dict(color=trace_color, width=2, shape="linear"),
            hovertemplate='%{x|%d.%m.%Y}<br>' + stage + ': %{y}<extra></extra>'
        ))
    fig_overall_cfd.update_layout(title="Overall GRA – Cumulative Flow Diagram (CFD)",
                                  xaxis_title="Date", yaxis_title="Count",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_cfd, use_container_width=True)
    
    # Aggregiere BDC-Daten
    dfs_bdc = []
    for dept in ["Gov", "Risk", "Audit"]:
        df = st.session_state[f"{dept}_BDC"].copy()
        df["Date"] = convert_date(df["Date"])
        dfs_bdc.append(df)
    df_overall_bdc = pd.concat(dfs_bdc).groupby("Date", as_index=False).sum()
    fig_overall_bdc = go.Figure()
    fig_overall_bdc.add_trace(go.Scatter(
        x=df_overall_bdc["Date"], y=df_overall_bdc["Ideal"],
        mode='lines', name='Ideal Burndown',
        line=dict(dash='dash', color='green'),
        hovertemplate='%{x|%d.%m.%Y}<br>Ideal: %{y}<extra></extra>'
    ))
    fig_overall_bdc.add_trace(go.Scatter(
        x=df_overall_bdc["Date"], y=df_overall_bdc["Actual"],
        mode='lines+markers', name='Actual Burndown',
        line=dict(color='red'),
        hovertemplate='%{x|%d.%m.%Y}<br>Actual: %{y}<extra></extra>'
    ))
    fig_overall_bdc.update_layout(title="Overall GRA – Burndown Chart (BDC)",
                                  xaxis_title="Date", yaxis_title="Work Remaining (%)",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_bdc, use_container_width=True)
    
    # Aggregiere BUC-Daten
    dfs_buc = []
    for dept in ["Gov", "Risk", "Audit"]:
        df = st.session_state[f"{dept}_BUC"].copy()
        df["Date"] = convert_date(df["Date"])
        dfs_buc.append(df)
    df_overall_buc = pd.concat(dfs_buc).groupby("Date", as_index=False).sum()
    fig_overall_buc = go.Figure()
    fig_overall_buc.add_trace(go.Scatter(
        x=df_overall_buc["Date"], y=df_overall_buc["Total Scope"],
        mode='lines', name='Total Scope',
        line=dict(color='purple'),
        hovertemplate='%{x|%d.%m.%Y}<br>Total Scope: %{y}<extra></extra>'
    ))
    fig_overall_buc.add_trace(go.Scatter(
        x=df_overall_buc["Date"], y=df_overall_buc["Completed"],
        mode='lines+markers', name='Completed',
        line=dict(color='orange'),
        hovertemplate='%{x|%d.%m.%Y}<br>Completed: %{y}<extra></extra>'
    ))
    fig_overall_buc.update_layout(title="Overall GRA – Burnup Chart (BUC)",
                                  xaxis_title="Date", yaxis_title="Work Units",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_buc, use_container_width=True)
    
    # EAC Diagramm (nur im Overall-Tab)
    df_overall_eac = st.session_state["EAC"].copy()
    df_overall_eac["Date"] = convert_date(df_overall_eac["Date"])
    df_overall_eac = df_overall_eac.sort_values("Date")
    fig_overall_eac = go.Figure()
    fig_overall_eac.add_trace(go.Scatter(
        x=df_overall_eac["Date"], y=df_overall_eac["Actual Cost"],
        mode='lines+markers', name='Actual Cost',
        line=dict(color='brown'),
        hovertemplate='%{x|%d.%m.%Y}<br>Actual Cost: %{y}<extra></extra>'
    ))
    fig_overall_eac.add_trace(go.Scatter(
        x=df_overall_eac["Date"], y=df_overall_eac["Forecast Cost"],
        mode='lines+markers', name='Forecast Cost',
        line=dict(dash='dash', color='gray'),
        hovertemplate='%{x|%d.%m.%Y}<br>Forecast Cost: %{y}<extra></extra>'
    ))
    fig_overall_eac.update_layout(title="Overall GRA – Estimate at Completion (EAC)",
                                  xaxis_title="Date", yaxis_title="Cost (€)",
                                  xaxis=dict(tickformat="%d.%m.%Y"))
    st.plotly_chart(fig_overall_eac, use_container_width=True)
    
    st.markdown("### Conclusion")
    st.markdown("""
    Die aggregierten Daten der Unterabteilungen werden hier zusammengeführt.
    Änderungen im Data Editor (Sidebar) wirken sich beim nächsten Rerun/Tabwechsel auf die Diagramme in den Abteilungstabs und der Overall-Ansicht aus.
    """)
else:
    dept_key = {"Governance": "Gov", "Risk": "Risk", "Audit & Assessment": "Audit"}[selected_dept]
    def render_charts_for_dept(dept_key, dept_name, color_scheme):
        st.markdown(f"### {dept_name} – Kennzahlen und Diagramme")
        # CFD
        df_cfd = st.session_state[f"{dept_key}_CFD"].copy()
        df_cfd["Date"] = convert_date(df_cfd["Date"])
        df_cfd = df_cfd.sort_values("Date")
        fig_cfd = go.Figure()
        for stage, col, trace_color in zip(["Backlog", "In Progress", "Done"],
                                           ["Backlog", "In Progress", "Done"],
                                           ["#1f77b4", "#ff7f0e", "#2ca02c"]):
            fig_cfd.add_trace(go.Scatter(
                x=df_cfd["Date"],
                y=df_cfd[col],
                mode="lines",
                name=stage,
                stackgroup="one",
                line=dict(color=trace_color, width=2, shape="linear"),
                hovertemplate='%{x|%d.%m.%Y}<br>' + stage + ': %{y}<extra></extra>'
            ))
        fig_cfd.update_layout(title=f"{dept_name} – Cumulative Flow Diagram (CFD)",
                              xaxis_title="Date", yaxis_title="Count",
                              xaxis=dict(tickformat="%d.%m.%Y"))
        st.plotly_chart(fig_cfd, use_container_width=True)
        
        # BDC
        df_bdc = st.session_state[f"{dept_key}_BDC"].copy()
        df_bdc["Date"] = convert_date(df_bdc["Date"])
        df_bdc = df_bdc.sort_values("Date")
        fig_bdc = go.Figure()
        fig_bdc.add_trace(go.Scatter(
            x=df_bdc["Date"], y=df_bdc["Ideal"],
            mode='lines', name='Ideal Burndown',
            line=dict(dash='dash', color='green'),
            hovertemplate='%{x|%d.%m.%Y}<br>Ideal: %{y}<extra></extra>'
        ))
        fig_bdc.add_trace(go.Scatter(
            x=df_bdc["Date"], y=df_bdc["Actual"],
            mode='lines+markers', name='Actual Burndown',
            line=dict(color='red'),
            hovertemplate='%{x|%d.%m.%Y}<br>Actual: %{y}<extra></extra>'
        ))
        fig_bdc.update_layout(title=f"{dept_name} – Burndown Chart (BDC)",
                              xaxis_title="Date", yaxis_title="Work Remaining (%)",
                              xaxis=dict(tickformat="%d.%m.%Y"))
        st.plotly_chart(fig_bdc, use_container_width=True)
        
        # BUC
        df_buc = st.session_state[f"{dept_key}_BUC"].copy()
        df_buc["Date"] = convert_date(df_buc["Date"])
        df_buc = df_buc.sort_values("Date")
        fig_buc = go.Figure()
        fig_buc.add_trace(go.Scatter(
            x=df_buc["Date"], y=df_buc["Total Scope"],
            mode='lines', name='Total Scope',
            line=dict(color=color_scheme),
            hovertemplate='%{x|%d.%m.%Y}<br>Total Scope: %{y}<extra></extra>'
        ))
        fig_buc.add_trace(go.Scatter(
            x=df_buc["Date"], y=df_buc["Completed"],
            mode='lines+markers', name='Completed',
            line=dict(color='orange'),
            hovertemplate='%{x|%d.%m.%Y}<br>Completed: %{y}<extra></extra>'
        ))
        fig_buc.update_layout(title=f"{dept_name} – Burnup Chart (BUC)",
                              xaxis_title="Date", yaxis_title="Work Units",
                              xaxis=dict(tickformat="%d.%m.%Y"))
        st.plotly_chart(fig_buc, use_container_width=True)
    
    render_charts_for_dept(dept_key, selected_dept, {"Governance": "blue", "Risk": "red", "Audit & Assessment": "green"}[selected_dept])
