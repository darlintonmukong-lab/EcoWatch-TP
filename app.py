import streamlit as st
import pandas as pd
import datetime
import os

# Configuration de la page
st.set_page_config(page_title="EcoWatch Pro", page_icon="🌍", layout="wide")

# Fichier de stockage permanent
DB_FILE = "data_collecte.csv"

# Charger les données existantes
if os.path.exists(DB_FILE):
    st.session_state.db = pd.read_csv(DB_FILE)
else:
    st.session_state.db = pd.DataFrame(columns=['Date', 'Type', 'Gravité', 'Quartier', 'Description'])

st.title("🌍 EcoWatch : Collecte & Analyse Environnementale")
st.markdown("---")

# --- SECTION 1 : COLLECTE ---
with st.sidebar:
    st.header("📝 Nouvelle Collecte")
    with st.form("form_signalement", clear_on_submit=True):
        type_pollution = st.selectbox("Type de pollution", ["Plastique", "Décharge sauvage", "Eaux usées", "Air", "Nuisance Sonore"])
        gravite = st.select_slider("Niveau de gravité", options=range(1, 11), value=5)
        quartier = st.text_input("Quartier", placeholder="Ex: Bastos, Melen...")
        description = st.text_area("Observations additionnelles")
        date_obs = st.date_input("Date de l'observation", datetime.date.today())
        submit = st.form_submit_button("Enregistrer le signalement")

if submit:
    if not quartier:
        st.error("La localisation est obligatoire.")
    else:
        new_entry = {'Date': str(date_obs), 'Type': type_pollution, 'Gravité': gravite, 'Quartier': quartier, 'Description': description}
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
        st.session_state.db.to_csv(DB_FILE, index=False)
        st.success("✅ Donnée enregistrée !")

# --- SECTION 2 : ANALYSE DESCRIPTIVE ---
if not st.session_state.db.empty:
    total_obs = len(st.session_state.db)
    moyenne = st.session_state.db['Gravité'].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Signalements", total_obs)
    col2.metric("Gravité Moyenne", f"{moyenne:.1f} / 10")
    
    if moyenne > 7: col3.error("🚨 État : Alerte Critique")
    elif moyenne > 4: col3.warning("⚠️ État : Vigilance")
    else: col3.success("✅ État : Stable")

    st.markdown("### 📊 Visualisation des données")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Répartition par type**")
        st.bar_chart(st.session_state.db['Type'].value_counts())
    with c2:
        st.write("**Évolution de la gravité**")
        st.line_chart(st.session_state.db.set_index('Date')['Gravité'])

    st.dataframe(st.session_state.db, use_container_width=True)
    csv = st.session_state.db.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Exporter les données (CSV)", data=csv, file_name="export_ecowatch.csv", mime="text/csv")
else:
    st.info("👋 Bienvenue ! Remplissez le formulaire à gauche.")

