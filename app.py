import streamlit as st
import pandas as pd
import os
import datetime

# 1. Infos Étudiant (Sidebar)
st.sidebar.title("🎓 Identification")
st.sidebar.info("Shiwun Mukong Darlinton\nMatricule : 24G2337")

# 2. Gestion des données
DB_FILE = "data_collecte.csv"
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=['Date', 'Type', 'Gravité', 'Quartier', 'Description'])

# 3. Interface Principale
st.title("🌍 EcoWatch Pro : Yaoundé Clean City")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Nouveau Signalement")
    with st.form("main_form", clear_on_submit=True):
        t_pollution = st.selectbox("Type de pollution", ["Plastique", "Décharge sauvage", "Eaux usées", "Fumée/Air"])
        
        # LISTE INTELLIGENTE DES QUARTIERS
        quartiers = ["Bastos", "Biyem-Assi", "Mendong", "Etoudi", "Ngousso", "Mvan", "Obili", "AUTRE..."]
        selection = st.selectbox("Quartier", quartiers)
        
        # Champ qui n'apparaît que si on choisit "AUTRE..."
        q_final = ""
        if selection == "AUTRE...":
            q_final = st.text_input("Précisez le quartier :")
        else:
            q_final = selection

        n_gravite = st.slider("Niveau de gravité (1-10)", 1, 10, 5)
        obs = st.text_area("Description")
        btn = st.form_submit_button("Enregistrer")

    if btn:
        new_row = {'Date': str(datetime.date.today()), 'Type': t_pollution, 'Gravité': n_gravite, 'Quartier': q_final, 'Description': obs}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("✅ Donnée enregistrée !")

with col2:
    st.subheader("📊 Analyse Descriptive")
    if not df.empty:
        st.metric("Total Signalements", len(df))
        st.metric("Gravité Moyenne", f"{df['Gravité'].mean():.1f}/10")
        
        # Le graphique qui va impressionner le prof
        st.bar_chart(df['Quartier'].value_counts())
    else:
        st.info("Ajoutez une donnée pour voir l'analyse.")

# Affichage du tableau en bas
st.markdown("---")
st.dataframe(df, use_container_width=True)
