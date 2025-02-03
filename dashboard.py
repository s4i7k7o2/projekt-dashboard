import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(layout="wide")

# --- Read Excel Data ---
data_file = "project_data.xlsx"

# Try to load data from Excel; if unavailable, use simulated data
try:
    df_cfd_excel = pd.read_excel(data_file, sheet_name="CFD", engine='openpyxl')
    df_bdc_excel = pd.read_excel(data_file, sheet_name="BDC", engine='openpyxl')
    df_buc_excel = pd.read_excel(data_file, sheet_name="BUC", engine='openpyxl')
    df_eac_excel = pd.read_excel(data_file, sheet_name="EAC", engine='openpyxl')
except Exception as e:
    st.error(f"Error loading Excel data: {e}")
    df_cfd_excel = df_bdc_excel = df_buc_excel = df_eac_excel = None

# Prepare CFD data (Cumulative Flow Diagram)
if df_cfd_excel is not None:
    df_cfd_plot = df_cfd_excel.melt(id_vars=["Date"],
                                    value_vars=["Backlog", "In Progress", "Done"],
                                    var_name="Stage",
                                    value_name="Count")
else:
    days = pd.date_range(start="2025-01-01", periods=20)
    backlog = np.random.randint(50, 100, size=20)
    in_progress = np.random.randint(20, 70, size=20)
    done = np.random.randint(10, 50, size=20)
    df_cfd_temp = pd.DataFrame({
        "Date": days,
        "Backlog": backlog,
        "In Progress": in_progress,
        "Done": done
    })
    df_cfd_plot = df_cfd_temp.melt(id_vars=["Date"],
                                   value_vars=["Backlog", "In Progress", "Done"],
                                   var_name="Stage",
                                   value_name="Count")

# Prepare BDC data (Burndown Chart)
if df_bdc_excel is not None:
    df_bdc_plot = df_bdc_excel.copy()
else:
    days = pd.date_range(start="2025-02-01", periods=15)
    ideal = np.linspace(100, 0, 15)
    actual = ideal + np.random.normal(0, 5, 15)
    df_bdc_plot = pd.DataFrame({
        "Date": days,
        "Ideal": ideal,
        "Actual": actual
    })

# Prepare BUC data (Burnup Chart)
if df_buc_excel is not None:
    df_buc_plot = df_buc_excel.copy()
else:
    days = pd.date_range(start="2025-03-01", periods=15)
    total_scope = np.linspace(100, 130, 15)
    completed = np.linspace(0, 100, 15) + np.random.normal(0, 5, 15)
    df_buc_plot = pd.DataFrame({
        "Date": days,
        "Total Scope": total_scope,
        "Completed": completed
    })

# Prepare EAC data (Estimate at Completion)
if df_eac_excel is not None:
    df_eac_plot = df_eac_excel.copy()
else:
    days = pd.date_range(start="2025-04-01", periods=15)
    actual_costs = np.linspace(0, 80000, 15) + np.random.normal(0, 2000, 15)
    forecast = actual_costs[-1] + np.linspace(0, 20000, 15)
    df_eac_plot = pd.DataFrame({
        "Date": days,
        "Actual Cost": actual_costs,
        "Forecast Cost": forecast
    })

# ----------------------
# Introduction and Definitions
# ----------------------
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
Compares contingency cost drawdown to project progress. Green means remaining contingency is likely adequate; yellow suggests closer monitoring; red indicates possible inadequacy.

**Safety Performance Metric (SPM)**  
Compares project safety performance to the industry national average, typically based on OSHA’s Incident Rate (IR).

**Quality Assurance Metric (QAM)**  
Assesses the contractor’s quality control program, often by comparing non-compliance notices or other quality indicators.
""")

# ----------------------
# Performance Metrics Gauges
# ----------------------
st.header("Performance Metrics Gauges")
st.markdown("The gauges below illustrate sample values for each performance metric category. In a real-world scenario, these values would be dynamically calculated based on project data.")

# Schedule Performance Metric Gauge
fig_schedule = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=75,  # sample value
    delta={'reference': 80, 'increasing': {'color': "red"}},
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
            'value': 80
        }
    }
))

# Cost Contingency Performance Metric Gauge
fig_cost = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=65,  # sample value
    delta={'reference': 70, 'increasing': {'color': "red"}},
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
            'value': 70
        }
    }
))

# Safety Performance Metric Gauge
fig_safety = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=90,  # sample value
    delta={'reference': 95, 'increasing': {'color': "red"}},
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
            'value': 95
        }
    }
))

# Quality Assurance Metric Gauge
fig_quality = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=80,  # sample value
    delta={'reference': 85, 'increasing': {'color': "red"}},
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
            'value': 85
        }
    }
))

# Layout the gauges in two columns
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_schedule, use_container_width=True)
    st.plotly_chart(fig_cost, use_container_width=True)
with col2:
    st.plotly_chart(fig_safety, use_container_width=True)
    st.plotly_chart(fig_quality, use_container_width=True)

# ----------------------
# Additional Diagrams Section
# ----------------------
st.header("Additional Diagrams")

# --- CFD: Cumulative Flow Diagram ---
st.subheader("CFD (Cumulative Flow Diagram)")
st.markdown("""
**When Useful:**  
- Particularly valuable in agile environments or ticket-driven processes to quickly identify bottlenecks in a specific phase.
- **Tip:** When combined with WIP (Work In Progress) limits, bottlenecks can be managed more effectively.
""")
fig_cfd = px.area(df_cfd_plot, x="Date", y="Count", color="Stage",
                  title="Cumulative Flow Diagram")
st.plotly_chart(fig_cfd, use_container_width=True)

# --- BDC: Burndown Chart ---
st.subheader("BDC (Burndown Chart)")
st.markdown("""
**When Useful:**  
- In time-boxed sprints/iterations, to track daily progress.
- **Tip:** Comparing the real burndown with the ideal (planned) line helps quickly spot deviations.
""")
fig_bdc = go.Figure()
fig_bdc.add_trace(go.Scatter(x=df_bdc_plot["Date"], y=df_bdc_plot["Ideal"],
                             mode='lines',
                             name='Ideal Burndown',
                             line=dict(dash='dash', color='green')))
fig_bdc.add_trace(go.Scatter(x=df_bdc_plot["Date"], y=df_bdc_plot["Actual"],
                             mode='lines+markers',
                             name='Actual Burndown',
                             line=dict(color='red')))
fig_bdc.update_layout(title="Burndown Chart (BDC)",
                      xaxis_title="Date",
                      yaxis_title="Work Remaining (%)")
st.plotly_chart(fig_bdc, use_container_width=True)

# --- BUC: Burnup Chart ---
st.subheader("BUC (Burnup Chart)")
st.markdown("""
**When Useful:**  
- When there are frequent scope changes. It shows progress as well as whether the overall project scope has changed.
- **Tip:** Ideal for project status meetings since it provides more information than a simple burndown, emphasizing “what is newly added.”
""")
fig_buc = go.Figure()
fig_buc.add_trace(go.Scatter(x=df_buc_plot["Date"], y=df_buc_plot["Total Scope"],
                             mode='lines',
                             name='Total Scope',
                             line=dict(color='blue')))
fig_buc.add_trace(go.Scatter(x=df_buc_plot["Date"], y=df_buc_plot["Completed"],
                             mode='lines+markers',
                             name='Completed Work',
                             line=dict(color='orange')))
fig_buc.update_layout(title="Burnup Chart (BUC)",
                      xaxis_title="Date",
                      yaxis_title="Work Units")
st.plotly_chart(fig_buc, use_container_width=True)

# --- EAC: Estimate at Completion ---
st.subheader("EAC (Estimate at Completion)")
st.markdown("""
**When Useful:**  
- When there are deviations in time or budget, to assess if corrective action is needed.
- **Tip:** Incorporating EAC into an Earned Value Management (EVM) framework yields a more robust cost and performance analysis.
""")
fig_eac = go.Figure()
fig_eac.add_trace(go.Scatter(x=df_eac_plot["Date"], y=df_eac_plot["Actual Cost"],
                             mode='lines+markers',
                             name='Actual Cost',
                             line=dict(color='purple')))
fig_eac.add_trace(go.Scatter(x=df_eac_plot["Date"], y=df_eac_plot["Forecast Cost"],
                             mode='lines+markers',
                             name='Forecast Cost',
                             line=dict(dash='dash', color='gray')))
fig_eac.update_layout(title="Estimate at Completion (EAC)",
                      xaxis_title="Date",
                      yaxis_title="Cost (€)")
st.plotly_chart(fig_eac, use_container_width=True)

# ----------------------
# Conclusion Section
# ----------------------
st.header("Conclusion")
st.markdown("""
In summary, using the PSR as a platform for regular performance presentations led by the project control manager and project executive is an effective method to engage decision makers. It helps address critical variances from the established baselines and documents the success or challenges of mitigation measures throughout the project lifecycle. The additional charts—CFD, BDC, BUC, and EAC—provide further insights that are essential for proactive project management and informed decision-making.
""")
