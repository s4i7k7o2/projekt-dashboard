import streamlit as st
import pandas as pd

st.set_page_config(page_title="GRA Reporting", layout="wide")

# Hilfsfunktion: Parsen eines Komma-separierten Strings in eine Liste von Zahlen
def parse_input_data(input_str):
    try:
        return [float(x.strip()) for x in input_str.split(',') if x.strip() != ""]
    except Exception as e:
        st.error("Fehler beim Parsen der Daten. Bitte Komma-separierte Zahlen eingeben.")
        return []

# Funktion, die in einem Tab die Eingabefelder und Diagramme (CFD, BDC, BUC) anzeigt.
def render_department_tab(department_name, prefix):
    st.header(department_name)
    # Wir nutzen zwei Spalten, um links (simulierte Sidebar) die Dateneingabe und rechts die Diagramme anzuzeigen.
    col_sidebar, col_charts = st.columns([1, 3])
    
    with col_sidebar:
        st.subheader("Daten eingeben")
        # Textfelder zur Eingabe der Daten (als Komma-separierte Zahlen)
        cfd_input = st.text_area("CFD Daten (z. B. 1,2,3,4,5)", key=f"{prefix}_cfd", value="1,2,3,4,5")
        bdc_input = st.text_area("BDC Daten (z. B. 5,4,3,2,1)", key=f"{prefix}_bdc", value="5,4,3,2,1")
        buc_input = st.text_area("BUC Daten (z. B. 1,2,3,4,5)", key=f"{prefix}_buc", value="1,2,3,4,5")
    
    with col_charts:
        # CFD Diagramm
        st.subheader("CFD Diagramm")
        cfd_data = parse_input_data(cfd_input)
        if cfd_data:
            df_cfd = pd.DataFrame({"Index": range(len(cfd_data)), "CFD": cfd_data})
            st.line_chart(df_cfd.set_index("Index"))
        else:
            st.info("Keine gültigen CFD-Daten vorhanden.")
            
        # BDC Diagramm
        st.subheader("BDC Diagramm")
        bdc_data = parse_input_data(bdc_input)
        if bdc_data:
            df_bdc = pd.DataFrame({"Index": range(len(bdc_data)), "BDC": bdc_data})
            st.line_chart(df_bdc.set_index("Index"))
        else:
            st.info("Keine gültigen BDC-Daten vorhanden.")
            
        # BUC Diagramm
        st.subheader("BUC Diagramm")
        buc_data = parse_input_data(buc_input)
        if buc_data:
            df_buc = pd.DataFrame({"Index": range(len(buc_data)), "BUC": buc_data})
            st.line_chart(df_buc.set_index("Index"))
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
        # Hier können zusätzlich EAC-Daten eingegeben werden – diese werden nur im Overall-Tab angezeigt.
        eac_input = st.text_area("EAC Daten (z. B. 10,9,8,7,6)", key="overall_eac", value="10,9,8,7,6")
        st.write("Aggregierte Daten aus Governance, Risk und Audit & Assessment werden automatisch berechnet.")
    
    with col_charts:
        aggregated_data = {}
        # Für die Diagrammtypen CFD, BDC, BUC werden die Daten aus den drei Unterabteilungen (sofern vorhanden) aggregiert.
        for chart in ["cfd", "bdc", "buc"]:
            data_list = []
            for dept in ["governance", "risk", "audit"]:
                key = f"{dept}_{chart}"
                # Prüfen, ob der jeweilige Schlüssel bereits in st.session_state vorhanden ist
                if key in st.session_state:
                    input_str = st.session_state[key]
                else:
                    # Falls in einem Untertab noch keine Eingabe erfolgt ist, wird ein Standardwert genutzt.
                    input_str = "0,0,0,0,0"
                parsed = parse_input_data(input_str)
                if parsed:
                    data_list.append(parsed)
            # Aggregation: Elementweise Summe (sofern alle Listen mindestens die gleiche Länge haben)
            if data_list:
                min_len = min(len(lst) for lst in data_list)
                trimmed = [lst[:min_len] for lst in data_list]
                aggregated = [sum(x) for x in zip(*trimmed)]
            else:
                aggregated = []
            aggregated_data[chart] = aggregated
        
        # Anzeigen der aggregierten Diagramme
        st.subheader("Aggregiertes CFD Diagramm")
        if aggregated_data["cfd"]:
            df_cfd = pd.DataFrame({"Index": range(len(aggregated_data["cfd"])), "CFD": aggregated_data["cfd"]})
            st.line_chart(df_cfd.set_index("Index"))
        else:
            st.info("Keine aggregierten CFD-Daten vorhanden.")
        
        st.subheader("Aggregiertes BDC Diagramm")
        if aggregated_data["bdc"]:
            df_bdc = pd.DataFrame({"Index": range(len(aggregated_data["bdc"])), "BDC": aggregated_data["bdc"]})
            st.line_chart(df_bdc.set_index("Index"))
        else:
            st.info("Keine aggregierten BDC-Daten vorhanden.")
            
        st.subheader("Aggregiertes BUC Diagramm")
        if aggregated_data["buc"]:
            df_buc = pd.DataFrame({"Index": range(len(aggregated_data["buc"])), "BUC": aggregated_data["buc"]})
            st.line_chart(df_buc.set_index("Index"))
        else:
            st.info("Keine aggregierten BUC-Daten vorhanden.")
        
        # EAC Diagramm (nur im Overall-Tab)
        st.subheader("EAC Diagramm")
        eac_data = parse_input_data(eac_input)
        if eac_data:
            df_eac = pd.DataFrame({"Index": range(len(eac_data)), "EAC": eac_data})
            st.line_chart(df_eac.set_index("Index"))
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
