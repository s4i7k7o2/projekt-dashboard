import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io

# Page configuration
st.set_page_config(layout="wide", page_title="GRA Dashboard")

# -------------------------------
# Helper Functions
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
    # Expects format DD.MM.YYYY and converts to datetime
    return pd.to_datetime(date_series, format='%d.%m.%Y', dayfirst=True)

# -------------------------------
# Default Data for Charts
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

def default_spm():
    # For SPM data: Planned and Earned values
    return pd.DataFrame({"Planned": [100], "Earned": [75]})

# -------------------------------
# Initialize Session State
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
if "SPM" not in st.session_state:
    st.session_state["SPM"] = default_spm()

# Example baseline values for additional metrics
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
# Sidebar: Department Selection and Data Editors
# -------------------------------
selected_dept = st.sidebar.selectbox(
    "Select a Department:",
    options=["GRA-Overall", "Governance", "Risk", "Audit & Assessment"]
)

if selected_dept == "GRA-Overall":
    st.sidebar.markdown("### Data Editor for Overall")
    with st.sidebar.expander("Edit EAC Data"):
        if data_editor is not None:
            edited_eac = data_editor(st.session_state["EAC"], num_rows="dynamic", key="EAC_editor")
        else:
            csv_text = st.text_area("EAC Data (CSV)", value=st.session_state["EAC"].to_csv(index=False), key="EAC_csv")
            try:
                edited_eac = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Error parsing CSV: {e}")
                edited_eac = st.session_state["EAC"]
        st.session_state["EAC"] = edited_eac
    with st.sidebar.expander("Edit SPM Data"):
        if data_editor is not None:
            edited_spm = data_editor(st.session_state["SPM"], num_rows="static", key="SPM_editor")
        else:
            csv_text = st.text_area("SPM Data (CSV)", value=st.session_state["SPM"].to_csv(index=False), key="SPM_csv")
            try:
                edited_spm = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Error parsing CSV: {e}")
                edited_spm = st.session_state["SPM"]
        st.session_state["SPM"] = edited_spm
else:
    dept_key = {"Governance": "Gov", "Risk": "Risk", "Audit & Assessment": "Audit"}[selected_dept]
    st.sidebar.markdown(f"### Data Editor for {selected_dept}")
    with st.sidebar.expander(f"{selected_dept} – CFD Data"):
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept_key}_CFD"], num_rows="dynamic", key=f"{dept_key}_CFD_editor")
        else:
            csv_text = st.text_area(f"CFD {selected_dept} (CSV)", value=st.session_state[f"{dept_key}_CFD"].to_csv(index=False), key=f"{dept_key}_CFD_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Error parsing CSV: {e}")
                edited = st.session_state[f"{dept_key}_CFD"]
        st.session_state[f"{dept_key}_CFD"] = edited

    with st.sidebar.expander(f"{selected_dept} – BDC Data"):
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept_key}_BDC"], num_rows="dynamic", key=f"{dept_key}_BDC_editor")
        else:
            csv_text = st.text_area(f"BDC {selected_dept} (CSV)", value=st.session_state[f"{dept_key}_BDC"].to_csv(index=False), key=f"{dept_key}_BDC_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Error parsing CSV: {e}")
                edited = st.session_state[f"{dept_key}_BDC"]
        st.session_state[f"{dept_key}_BDC"] = edited

    with st.sidebar.expander(f"{selected_dept} – BUC Data"):
        if data_editor is not None:
            edited = data_editor(st.session_state[f"{dept_key}_BUC"], num_rows="dynamic", key=f"{dept_key}_BUC_editor")
        else:
            csv_text = st.text_area(f"BUC {selected_dept} (CSV)", value=st.session_state[f"{dept_key}_BUC"].to_csv(index=False), key=f"{dept_key}_BUC_csv")
            try:
                edited = pd.read_csv(io.StringIO(csv_text), sep=",")
            except Exception as e:
                st.error(f"Error parsing CSV: {e}")
                edited = st.session_state[f"{dept_key}_BUC"]
        st.session_state[f"{dept_key}_BUC"] = edited

# -------------------------------
# Main Area: Display Charts
# -------------------------------
st.title(f"{selected_dept} Dashboard")

def render_charts_for_dept(dept_key, dept_name, color_scheme):
    st.markdown(f"### {dept_name} – Charts and Metrics")
    
    # CFD Chart Description
    st.markdown("**CFD (Cumulative Flow Diagram):** This diagram shows the evolution over time of the counts in the statuses 'Backlog', 'In Progress', and 'Done'. It displays how the total number of entries changes over time.")
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
    
    # BDC Chart Description
    st.markdown("**BDC (Burndown Chart):** This chart compares the ideal course of work remaining with the actual progress over time.")
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
    
    # BUC Chart Description
    st.markdown("**BUC (Burnup Chart):** This chart displays the total project scope and the completed portion over time, reflecting both progress and scope changes.")
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

# Render charts based on Sidebar selection
if selected_dept == "GRA-Overall":
    st.markdown("### Overall GRA – Aggregated Charts and Metrics")
    
    # Gauge Charts for SPM and CCPM at the top
    st.markdown("**Performance Metrics Gauges:** These gauges provide a quick overview of project performance. The SPM (Schedule Performance Metric) indicates field progress versus planned progress, and the CCPM (Cost Contingency Performance Metric) is calculated based on aggregated EAC data.")
    # SPM: SPM = (Earned / Planned)*100, using SPM data from the SPM Data Editor
    spm_df = st.session_state["SPM"]
    spm_value = (spm_df["Earned"].iloc[0] / spm_df["Planned"].iloc[0]) * 100
    spm_value = round(spm_value, 2)
    spm_ref = 100
    # CCPM: calculated from the aggregated EAC data (last record)
    df_eac = st.session_state["EAC"].copy()
    df_eac["Date"] = convert_date(df_eac["Date"])
    df_eac = df_eac.sort_values("Date")
    last_row = df_eac.iloc[-1]
    ccp_value = (last_row["Actual Cost"] / last_row["Forecast Cost"]) * 100
    ccp_value = round(ccp_value, 2)
    ccp_ref = 100

    col1, col2 = st.columns(2)
    fig_spm = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=spm_value,
        delta={'reference': spm_ref},
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
                'value': spm_ref
            }
        }
    ))
    fig_ccpm = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ccp_value,
        delta={'reference': ccp_ref},
        title={'text': "Cost Contingency Performance Metric (CCPM)"},
        gauge={
            'axis': {'range': [0, 150]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 150], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': ccp_ref
            }
        }
    ))
    with col1:
        st.plotly_chart(fig_spm, use_container_width=True)
    with col2:
        st.plotly_chart(fig_ccpm, use_container_width=True)
    
    # Aggregated CFD Description
    st.markdown("**CFD (Cumulative Flow Diagram):** This diagram displays the cumulative count of items in the statuses 'Backlog', 'In Progress', and 'Done' over time, showing the total number of entries at each point.")
    # Aggregated CFD Data
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
    
    # Aggregated BDC Description
    st.markdown("**BDC (Burndown Chart):** This chart compares the ideal burndown (planned progress) with the actual progress over time.")
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
    
    # Aggregated BUC Description
    st.markdown("**BUC (Burnup Chart):** This chart illustrates the total project scope and the completed work over time, reflecting overall progress and scope changes.")
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
    
    # EAC Diagram Description
    st.markdown("**EAC (Estimate at Completion):** This chart compares the actual cost with the forecast cost over time, helping to determine if any corrective actions are required.")
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
    The aggregated data from the sub-departments is combined here.
    Changes in the data editors (sidebar) will be reflected in the charts after a rerun or tab change.
    """)
else:
    dept_key = {"Governance": "Gov", "Risk": "Risk", "Audit & Assessment": "Audit"}[selected_dept]
    def render_charts_for_dept(dept_key, dept_name, color_scheme):
        st.markdown(f"### {dept_name} – Charts and Metrics")
        # CFD Description
        st.markdown("**CFD (Cumulative Flow Diagram):** This diagram shows the evolution of the counts in 'Backlog', 'In Progress', and 'Done' over time.")
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
        
        # BDC Description
        st.markdown("**BDC (Burndown Chart):** This chart compares the ideal burndown with the actual progress over time.")
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
        
        # BUC Description
        st.markdown("**BUC (Burnup Chart):** This chart displays the total project scope and the completed portion over time, indicating progress and any scope changes.")
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
