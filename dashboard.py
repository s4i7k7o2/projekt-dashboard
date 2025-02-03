import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="GRA Reporting", layout="wide")

# Hilfsfunktion: Parsen eines Komma-separierten Strings in eine Liste von Zahlen
def parse_input_data(input_str):
    try:
        return [float(x.strip()) for x in input_str.split(',') if x.strip() != ""]
    except Exception as e:
        st.error("Fehler beim Parsen der Daten. Bitte Komma-separierte Zahlen eingeben.")
        return []

# Funktion für ein interaktives CFD Diagramm (als Linien-Chart mit Markern)
def plot_cfd(data, title="CFD Diagramm"):
    df = pd.DataFrame({'Index': range(len(data)), 'Wert': data})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Index'], y=df['Wert'],
                             mode='lines+markers',
                             marker=dict(size=8),
                             line=dict(width=2),
                             name="CFD"))
    fig.update_layout(title=title,
                      xaxis_title='Index',
                      yaxis_title='Wert',
                      template="plotly_white")
    return fig

# Funktion für ein interaktives BDC Diagramm (Burndown)
def plot_bdc(data, title="BDC Diagramm"):
    df = pd.DataFrame({'Index': range(len(data)), 'Wert': data})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Index'], y=df['Wert'],
                             mode='lines+markers',
                             marker=dict(size=8),
                             line=dict(width=2),
                             name="BDC"))
    fig.update_layout(title=title,
                      xaxis_title='Index',
                      yaxis_title='Wert',
                      template="plotly_white")
    return fig

# Funktion für ein interaktives BUC Diagramm (Burnup)
def plot_buc(data, title="BUC Diagramm"):
    df = pd.DataFrame({'Index': range(len(data)), 'Wert': data})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Index'], y=df['Wert'],
                             mode='lines+markers',
                             marker=dict(size=8),
                             line=dict(width=2),
                             name="BUC"))
    fig.update_layout(title=title,
                      xaxis_title='Index',
                      yaxis_title='Wert',
                      template="plotly_white")
    return fig

# Funktion für das EAC Diagramm
def plot_eac(data, title="EAC Diagramm"):
    df = pd.DataFrame({'Index': range(len(data)), 'Wert': data})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Index'], y=df['Wert'],
                             mode='lines+markers',
                             marker=dict(size=8),
                             line=dict(width=2),
                             name="EAC"))
    fig.update_layout(title=title,
                      xaxis_title='Index',
                      yaxis_title='Wert',
                      template="plotly_white")
    return fig

# Funktion, die in einem Tab die Eingabefelder und Diagramme (CFD, BDC, BUC) anzeigt.
def render_department_tab(department_name, prefix):
    st.header(department_name)
    col_sidebar, col_charts = st.columns([1, 3])
    
    with col_sidebar:
        st.subheader("Daten eingeben")
        cfd_input = st.text_area("CFD Daten (z. B. 1,2,3,4,5)", key=f"{prefix}_cfd", value="1,2,3,4,5")
        bdc_input = st.text_area("BDC Daten (z. B. 5,4,3,2,1)", key=f"{prefix}_bdc", value="5,4,3,2,1")
        buc_input = st.text_area("BUC Daten (z. B. 1,2,3,4,5)", key=f"{prefix}_buc", value="1,2,3,4,5")
    
    with col_charts:
        st.subheader("CFD Diagramm")
        cfd_data = parse_input_data(cfd_input)
        if cfd_data:
            fig = plot_cfd(cfd_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine gültigen CFD-Daten vorhanden.")
            
        st.subheader("BDC Diagramm")
        bdc_data = parse_input_data(bdc_input)
        if bdc_data:
            fig = plot_bdc(bdc_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine gültigen BDC-Daten vorhanden.")
            
        st.subheader("BUC Diagramm")
        buc_data = parse_input_data(buc_input)
        if buc_data:
            fig = plot_buc(buc_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine gültigen BUC-Daten vorhanden.")
            
        with st.expander("Weitere Diagramme"):
            st.write("• Gantt Chart (Platzhalter)")
            st.write("• Heatmap (Platzhalter)")
            st.write("• Dashboard (Platzhalter)")

# Funktion, die im Overall-Tab die aggregierten Daten der drei Unterabteilungen anzeigt
def render_overall_tab():
    st.header("GRA (Overall)")
    col_sidebar, col_charts = st.columns([1, 3])
    
    with col_sidebar:
        st.subheader("Daten eingeben")
        eac_input = st.text_area("EAC Daten (z. B. 10,9,8,7,6)", key="overall_eac", value="10,9,8,7,6")
        st.write("Aggregierte Daten aus Governance, Risk und Audit & Assessment werden automatisch berechnet.")
    
    with col_charts:
        aggregated_data = {}
        # Aggregation für CFD, BDC und BUC aus den drei Unterabteilungen
        for chart in ["cfd", "bdc", "buc"]:
            data_list = []
            for dept in ["governance", "risk", "audit"]:
                key = f"{dept}_{chart}"
                if key in st.session_state:
                    input_str = st.session_state[key]
                else:
                    # Falls in einem Untertab noch keine Eingabe erfolgt ist, wird ein Standardwert genutzt.
                    input_str = "0,0,0,0,0"
                parsed = parse_input_data(input_str)
                if parsed:
                    data_list.append(parsed)
            if data_list:
                min_len = min(len(lst) for lst in data_list)
                trimmed = [lst[:min_len] for lst in data_list]
                aggregated = [sum(x) for x in zip(*trimmed)]
            else:
                aggregated = []
            aggregated_data[chart] = aggregated
        
        st.subheader("Aggregiertes CFD Diagramm")
        if aggregated_data["cfd"]:
            fig = plot_cfd(aggregated_data["cfd"], title="Aggregiertes CFD Diagramm")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine aggregierten CFD-Daten vorhanden.")
        
        st.subheader("Aggregiertes BDC Diagramm")
        if aggregated_data["bdc"]:
            fig = plot_bdc(aggregated_data["bdc"], title="Aggregiertes BDC Diagramm")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine aggregierten BDC-Daten vorhanden.")
            
        st.subheader("Aggregiertes BUC Diagramm")
        if aggregated_data["buc"]:
            fig = plot_buc(aggregated_data["buc"], title="Aggregiertes BUC Diagramm")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine aggregierten BUC-Daten vorhanden.")
        
        st.subheader("EAC Diagramm")
        eac_data = parse_input_data(eac_input)
        if eac_data:
            fig = plot_eac(eac_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Keine gültigen EAC-Daten vorhanden.")
        
        with st.expander("Weitere Diagramme"):
            st.write("• Gantt Chart (Platzhalter)")
            st.write("• Heatmap (Platzhalter)")
            st.write("• Dashboard (Platzhalter)")

# Erstellen der vier Tabs
tab_governance, tab_risk, tab_audit, tab_overall = st.tabs([
    "Governance", 
    "Risk", 
    "Audit & Assessment", 
    "GRA (Overall)"
])

with tab_governance:
    render_department_tab("Governance", "governance")

with tab_risk:
    render_department_tab("Risk", "risk")

with tab_audit:
    render_department_tab("Audit & Assessment", "audit")

with tab_overall:
    render_overall_tab()
