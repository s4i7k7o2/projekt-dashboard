import streamlit as st
import plotly.graph_objects as go

# Set wide layout for the dashboard
st.set_page_config(layout="wide")

# Title and Introduction
st.title("Project Performance Dashboard")

st.header("Introduction")
st.markdown("""
Project-status reporting is intended to enable decision makers to make informed decisions that will increase the chances of achieving a favorable outcome. Furthermore, it is a vehicle to communicate project performance information to project stakeholders.

The information portrayed in the Project Status Report (PSR) pertains to variances from the original project baseline plans for schedule, cost, quality, and safety.

An effective PSR will command the attention of project executives and decision makers, and help focus their attention on critical deviations from the project’s baseline plans that pose risks to achieving a favorable project outcome.

Unfortunately, PSRs are seldom read by project executives and are often shelved upon issuance.

The underutilization of this project tool, which is intended to be a key to project success, is rooted in a multitude of reasons including:

- **Report content:** Issues that are common knowledge to the project team (yesterday’s news) should be addressed in terms of how effective the current mitigation measures being employed to correct them are, while newly evolving issues should be clearly identified along with a discussion of potential mitigation measures to correct them.
- **Presentation of project data:** The content of a PSR is paramount; however, the effectiveness and reach of the message lies in the presentation of the project performance data.
- **Timeliness of PSRs:** The timeliness of publishing the PSR is vital in a fast-moving project environment. Timely decisions to mitigate project risks are critical to formulating a successful solution.

This article will discuss the process of establishing an effective reporting system that ensures proactive project-status reporting and engagement of the project executive team to maximize the chances of project success.
""")

st.header("Definitions")
st.markdown("""
**Schedule Performance Metric (SPM)**  
This is an indicator of field progress versus planned progress. If the indicator falls within the green range, the project is on or ahead of schedule; if it falls within the yellow range, the project is starting to fall behind schedule; if it falls within the red range, the project is significantly behind schedule and warrants corrective action. The SPM is calculated as the ratio between the dollar amount earned and the dollar amount planned.

**Cost Contingency Performance Metric (CCPM)**  
This indicator compares contingency cost drawdown to project progress to date. If the indicator is in the green range, the remaining contingency cost is likely adequate; yellow indicates that closer monitoring is warranted; and red suggests that a quantitative risk analysis may be needed to determine additional contingency.

**Safety Performance Metric (SPM)**  
This metric compares the safety performance of the project to the industry national average. It is typically based on the Incident Rate (IR) as defined by OSHA.

**Quality Assurance Metric (QAM)**  
The QAM assesses the contractor’s quality control program. It may focus on a single aspect or incorporate several aspects, such as the number of non-compliance notices issued relative to expectations.
""")

st.header("Performance Metrics Gauges")
st.markdown("The gauges below illustrate sample values for each performance metric category. In a real-world scenario, these values would be dynamically calculated based on project data.")

# --- Schedule Performance Metric Gauge ---
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

# --- Cost Contingency Performance Metric Gauge ---
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

# --- Safety Performance Metric Gauge ---
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

# --- Quality Assurance Metric Gauge ---
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

st.header("Conclusion")
st.markdown("""
In summary, using the PSR as a platform for regular performance presentations organized by the project control manager and headed by the project executive is an effective way to engage project executives and functional managers to address critical variances from the established project baselines that will likely impact the project outcomes. This approach can also be used to document the successful or unsuccessful results of mitigation measures and corrective actions over the course of the project life cycle, which is a very valuable benefit to any organization that endorses a continuous improvement process.
""")
