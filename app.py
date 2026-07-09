"""Suivi de migration ERP/CRM & gestion du changement — POC personnel.
Plan de cutover, réconciliation des données migrées, suivi des tickets
support pendant la période d'hypercare post go-live.
"""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data.demo_data import generate_taches_cutover, generate_reconciliation_donnees, generate_tickets_hypercare

C_PRIMARY = "#0071E3"
C_GOOD    = "#34C759"
C_WARNING = "#FF9F0A"
C_DANGER  = "#FF3B30"
C_SURF    = "#F5F5F7"
C_TEXT    = "#1D1D1F"
C_MUTED   = "#6E6E73"
C_BORDER  = "#E8E8ED"

STATUT_TACHE_COLORS = {"Termine": C_GOOD, "En cours": C_WARNING, "A faire": C_MUTED, "Bloque": C_DANGER}
STATUT_RECON_COLORS = {"Conforme": C_GOOD, "A verifier": C_WARNING, "Ecart significatif": C_DANGER}

CHART_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=C_TEXT, family="Inter, -apple-system, sans-serif", size=13),
    margin=dict(l=20, r=20, t=40, b=20),
)

st.set_page_config(page_title="Migration ERP/CRM & Change Management", page_icon="🔀",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
html, body, [class*="css"] { font-family:'Inter',-apple-system,sans-serif; }
div[data-testid="stMetricValue"] { font-size: 1.7rem; font-weight: 700; }
.stTabs [aria-selected="true"] { font-weight: 700; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_all():
    return generate_taches_cutover(), generate_reconciliation_donnees(), generate_tickets_hypercare()


taches, recon, tickets = load_all()

with st.sidebar:
    st.markdown(
        "<div style='text-align:center;padding:12px 0;'>"
        "<div style='font-size:1.8rem;'>🔀</div>"
        f"<div style='color:{C_PRIMARY};font-size:1.05rem;font-weight:700;'>Migration ERP/CRM</div>"
        f"<div style='color:{C_MUTED};font-size:0.72rem;'>Cutover & hypercare</div>"
        "</div>", unsafe_allow_html=True)
    st.markdown(f"<hr style='border-color:{C_BORDER};'>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='background:{C_SURF};border-radius:8px;padding:10px;font-size:0.75rem;color:{C_MUTED};'>"
        "⚠️ <strong>Projet personnel (POC)</strong><br>"
        "Démonstration de compétences — données simulées, aucun outil ERP/CRM propriétaire connecté."
        "</div>", unsafe_allow_html=True)

st.title("Suivi de migration ERP/CRM & gestion du changement")
st.caption("Plan de cutover, réconciliation des données migrées, suivi des tickets support pendant l'hypercare.")

tabs = st.tabs(["Plan de cutover", "Réconciliation données", "Hypercare (support)"])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tâches totales", len(taches))
    c2.metric("Terminées", len(taches[taches["statut"] == "Termine"]))
    c3.metric("Bloquées", len(taches[taches["statut"] == "Bloque"]), delta_color="inverse")
    en_retard = len(taches[(taches["statut"] != "Termine") & (pd.to_datetime(taches["echeance"]).dt.date < pd.Timestamp.now().date())])
    c4.metric("En retard", en_retard, delta_color="inverse")

    for phase in ["Extraction", "Transformation", "Chargement", "Validation"]:
        t = taches[taches["phase"] == phase]
        if t.empty:
            continue
        done = len(t[t["statut"] == "Termine"])
        pct = int(done / len(t) * 100)
        st.markdown(f"**{phase}** — {pct}% ({done}/{len(t)})")
        st.markdown(
            f"<div style='background:{C_BORDER};border-radius:6px;height:8px;margin-bottom:14px;'>"
            f"<div style='background:{C_PRIMARY};width:{pct}%;height:8px;border-radius:6px;'></div></div>",
            unsafe_allow_html=True)

    bloquees = taches[taches["statut"] == "Bloque"]
    if not bloquees.empty:
        st.markdown("#### ⚠️ Tâches bloquées")
        st.dataframe(bloquees, use_container_width=True, hide_index=True)

with tabs[1]:
    st.markdown("### Réconciliation des enregistrements migrés")
    for _, r in recon.iterrows():
        color = STATUT_RECON_COLORS[r["statut"]]
        st.markdown(
            f"<div style='background:#fff;border-left:4px solid {color};border-radius:0 8px 8px 0;"
            f"padding:14px 18px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04);'>"
            f"<strong>{r['module']}</strong> — <span style='color:{color};'>{r['statut']}</span><br>"
            f"<span style='color:{C_MUTED};font-size:0.85rem;'>{r['enregistrements_avant']:,} → "
            f"{r['enregistrements_apres']:,} enregistrements ({r['ecart_pct']:+.1f}%)</span>"
            f"</div>".replace(",", " "),
            unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=recon["module"], y=recon["enregistrements_avant"], name="Avant migration", marker_color=C_MUTED))
    fig.add_trace(go.Bar(x=recon["module"], y=recon["enregistrements_apres"], name="Après migration", marker_color=C_PRIMARY))
    fig.update_layout(title="Comparaison avant/après par module", barmode="group", height=380, **CHART_DEFAULTS)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.markdown("### Volume de tickets support — période d'hypercare")
    par_jour = tickets.groupby("date").size().reset_index(name="tickets")
    fig = go.Figure(go.Scatter(x=par_jour["date"], y=par_jour["tickets"], mode="lines+markers",
                               line=dict(color=C_WARNING, width=3), fill="tozeroy"))
    fig.update_layout(title="Tickets par jour depuis le go-live", height=360, **CHART_DEFAULTS)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        rep_type = tickets["type"].value_counts()
        fig = go.Figure(go.Bar(x=rep_type.values, y=rep_type.index, orientation="h", marker_color=C_PRIMARY))
        fig.update_layout(title="Répartition par type de ticket", height=300, **CHART_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        taux_resolution = tickets["resolu"].mean() * 100
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=taux_resolution,
            title={"text": "Taux de résolution (%)"},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": C_GOOD}},
        ))
        fig.update_layout(height=300, **CHART_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)

    st.info("💡 La décroissance du volume de tickets sur la période reflète l'adoption progressive des utilisateurs — un pic élevé et durable signalerait un besoin de formation complémentaire.")
