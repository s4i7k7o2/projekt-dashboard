import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import io

# Set page configuration
st.set_page_config(layout="wide")

# Utility: Try to use a data editor widget if available.
def get_data_editor():
    if hasattr(st, "experimental_data_editor"):
        return st.experimental_data_editor
    elif hasattr(st, "data_editor"):
        return st.data_editor
    else:
        return None

data_editor = get_data_editor()

# Initialize session state keys for performance metrics if not already set.
if "spm_value" not in st.session_state:
    st.session_state.spm_value = 75
if "spm_ref" not in st.session_state:
    st.session_state.spm_ref = 80
if "ccpm_value" not in st.session_state:
    st.session_state.ccpm_value = 65
if "ccpm_ref" not in st.session_state:
    st.session_state.ccpm_ref = 70
if "safety_value" not in st.session_state:
    st.session_state.safety_value = 90
if "safety_ref" not in st.session_state:
    st.session_state.safety_ref = 95
if "qam_value" not in st.session_state:
    st.session_state.qam_value = 80
if "qam_ref" not in st.session_state:
    st.session_state.qam_ref = 85

# Create two tabs: one for the Dashboard and one for Data Editor.
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
    Compares contingency cost drawdown to project progress. Green means remaining contingency is likely adequate; yellow suggests closer monitoring; red indicates possible inadequacy.
    
    **Safety Performance Metric (SPM)**  
    Compares project safety performance to the industry national average, typically based on OSHA’s Incident Rate (IR).
    
    **Quality Assurance Metric (QAM)**  
    Assesses the contractor’s quality control program, often by comparing non-compliance notices or other quality indicators.
    """)

    # ----------------------
    # Performance Metrics Gauges (using session state values)
    # ----------------------
    st.header("Performance Metrics Gauges")
    st.markdown("The gauges below illustrate performance metric values based on the data entered in the Data Editor tab.")
    
    # Schedule Performance Metric Gauge (SPM)
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

    # Cost Contingency Performance Metric Gauge (CCPM)
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

    # Safety Performance Metric Gauge (Safety SPM)
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

    # Quality Assurance Metric Gauge (QAM)
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

    # Layout the gauges in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_schedule, use_container_width=True)
        st.plotly_chart(fig_cost, use_container_width=True)
    with col2:
        st.plotly_chart(fig_safety, use_container_width=True)
        st.plotly_chart(fig_quality, use_container_width=True)

    # ----------------------
    # Additional Diagrams Section (using simulated chart data)
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
    In summary, using the PSR as a platform for regular performance presentations led by the project control manager and project executive is an effective method to engage decision makers. It helps address critical variances from established baselines and documents the success or challenges of mitigation measures throughout the project lifecycle. The additional charts (CFD, BDC, BUC, and EAC) provide further insights essential for proactive project management.
    """)

# ===========================
# TAB 2: DATA EDITOR
# ===========================
with tabs[1]:
    st.title("Manual Data Entry")
    st.markdown("In this tab you can manually edit the sample data. Changes here will update the Dashboard tab.")
    
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
        st.info("Data editor widget not available. Edit CSV below.")
        csv_cfd = sample_cfd.to_csv(index=False)
        edited_csv_cfd = st.text_area("Edit CFD data (CSV)", value=csv_cfd, key="cfd_txt")
        try:
            edited_cfd = pd.read_csv(io.StringIO(edited_csv_cfd))
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
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
        st.info("Data editor widget not available. Edit CSV below.")
        csv_bdc = sample_bdc.to_csv(index=False)
        edited_csv_bdc = st.text_area("Edit BDC data (CSV)", value=csv_bdc, key="bdc_txt")
        try:
            edited_bdc = pd.read_csv(io.StringIO(edited_csv_bdc))
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
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
        st.info("Data editor widget not available. Edit CSV below.")
        csv_buc = sample_buc.to_csv(index=False)
        edited_csv_buc = st.text_area("Edit BUC data (CSV)", value=csv_buc, key="buc_txt")
        try:
            edited_buc = pd.read_csv(io.StringIO(edited_csv_buc))
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
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
        st.info("Data editor widget not available. Edit CSV below.")
        csv_eac = sample_eac.to_csv(index=False)
        edited_csv_eac = st.text_area("Edit EAC data (CSV)", value=csv_eac, key="eac_txt")
        try:
            edited_eac = pd.read_csv(io.StringIO(edited_csv_eac))
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
            edited_eac = sample_eac

    st.header("Performance Metrics Data")
    st.markdown("Update the performance metric values. These values are used by the gauges in the Dashboard tab.")
    st.session_state.spm_value = st.number_input("SPM Value (0-100)", value=st.session_state.spm_value, key="spm_value_input")
    st.session_state.spm_ref   = st.number_input("SPM Reference", value=st.session_state.spm_ref, key="spm_ref_input")
    st.session_state.ccpm_value = st.number_input("CCPM Value (0-100)", value=st.session_state.ccpm_value, key="ccpm_value_input")
    st.session_state.ccpm_ref   = st.number_input("CCPM Reference", value=st.session_state.ccpm_ref, key="ccpm_ref_input")
    st.session_state.safety_value = st.number_input("Safety SPM Value (0-100)", value=st.session_state.safety_value, key="safety_value_input")
    st.session_state.safety_ref   = st.number_input("Safety SPM Reference", value=st.session_state.safety_ref, key="safety_ref_input")
    st.session_state.qam_value = st.number_input("QAM Value (0-100)", value=st.session_state.qam_value, key="qam_value_input")
    st.session_state.qam_ref   = st.number_input("QAM Reference", value=st.session_state.qam_ref, key="qam_ref_input")
    
    st.markdown("Changes here will update the charts in the Dashboard tab on the next rerun.")
