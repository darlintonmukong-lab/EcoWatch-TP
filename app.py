import streamlit as st
import pandas as pd
import os
import datetime

# 1. Configuration FORCÉE en mode Large
st.set_page_config(page_title="EcoWatch Pro", page_icon="🌱", layout="wide")

# 2. Gestion des données
DB_FILE = "data_collecte.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=['Date', 'Type', 'Gravité', 'Quartier', 'Description'])

# 3. En-tête avec Identification
st.title("🌍 EcoWatch Pro : Yaoundé Clean City")
st.info(f"**Étudiant :** Shiwun Mukong Darlinton | **Matricule :** 24G2337")

# MESSAGE DE BIENVENUE (Ton souhait)
st.warning("👋 Bienvenue ! Veuillez remplir le formulaire dans la colonne de gauche. L'analyse descriptive à droite se mettra à jour automatiquement.")

st.markdown("---")

# 4. Création de deux colonnes équilibrées
col_gauche, col_droite = st.columns([1, 1], gap="large")

with col_gauche:
    st.subheader("📝 Nouveau Signalement")
    with st.form("main_form", clear_on_submit=True):
        type_p = st.selectbox("Type de pollution", ["Plastique", "Décharge sauvage", "Eaux usées", "Fumée/Air"])
        
        quartiers = ["Bastos", "Biyem-Assi", "Mendong", "Etoudi", "Ngousso", "Mvan", "Obili", "AUTRE..."]
        selection = st.selectbox("Quartier", quartiers)
        
        q_final = ""
        if selection == "AUTRE...":
            q_final = st.text_input("Précisez le quartier :")
        else:
            q_final = selection

        n_gravite = st.select_slider("Niveau de gravité (1-10)", options=range(1, 11), value=5)
        obs = st.text_area("Description / Observations")
        
        btn = st.form_submit_button("ENREGISTRER LE SIGNALEMENT", use_container_width=True)

    if btn:
        new_row = {'Date': str(datetime.date.today()), 'Type': type_p, 'Gravité': n_gravite, 'Quartier': q_final, 'Description': obs if obs else "RAS"}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.balloons()
        st.success("✅ Donnée enregistrée avec succès !")
        st.rerun()

with col_droite:
    st.subheader("📊 Analyse Descriptive")
    if not df.empty:
        # Métriques en ligne
        m1, m2 = st.columns(2)
        m1.metric("Total Signalements", len(df))
        m2.metric("Gravité Moyenne", f"{df['Gravité'].mean():.1f}/10")
        
        st.markdown("---")
        # Graphique
        st.write("**Répartition par Quartier :**")
        st.bar_chart(df['Quartier'].value_counts())
    else:
        st.info("En attente de données pour générer les graphiques...")

# 5. Historique en bas
st.markdown("---")
st.write("### 📂 Historique des données")
st.dataframe(df, use_container_width=True)
