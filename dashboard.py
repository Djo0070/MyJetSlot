import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_bookings

def show():
    st.markdown("<h1 style='text-align: center;'>📊 Tableau de bord</h1>", unsafe_allow_html=True)
    
    # Si l'utilisateur n'est pas connecté, afficher un tableau de bord vide
    if "user" not in st.session_state or st.session_state.user is None:
        st.info("💡 Connectez-vous pour voir vos réservations personnelles.")
        # Afficher un aperçu public (ex: statistiques globales)
        st.markdown("### 📈 Aperçu du service")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✈️ Créneaux disponibles", "12")
        with col2:
            st.metric("🚢 Ports partenaires", "8")
        with col3:
            st.metric("📅 Réservations aujourd'hui", "3")
        return
    
    bookings = get_bookings(st.session_state.user['localId'])
    
    # ============================================
    # STATISTIQUES UTILISATEUR (AJOUTÉ)
    # ============================================
    st.markdown("### 👤 Vos statistiques")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total réservations", len(bookings) if bookings else 0)
    
    with col2:
        # Compter les réservations confirmées
        confirmed = sum(1 for b in bookings if b.get('status') == 'confirmed') if bookings else 0
        st.metric("✅ Confirmées", confirmed)
    
    with col3:
        # Compter les réservations en attente
        pending = sum(1 for b in bookings if b.get('status') == 'pending') if bookings else 0
        st.metric("⏳ En attente", pending)
    
    st.divider()
    
    if bookings:
        df = pd.DataFrame(bookings)
        
        # Graphique
        if 'date' in df.columns:
            fig = px.bar(df, x='date', color='type', title="Réservations par date")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 Dernières réservations")
        for b in bookings[:5]:
            st.info(f"**{b['type']}** - {b['location']} - {b['date']} à {b['time']} ({b['status']})")
    else:
        st.info("Aucune réservation. Effectuez votre première réservation !")
    
    # ============================================
    # APERÇU GLOBAL DU SERVICE (AJOUTÉ EN BAS)
    # ============================================
    st.divider()
    st.markdown("### 📈 Aperçu global du service")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✈️ Créneaux disponibles", "12")
    with col2:
        st.metric("🚢 Ports partenaires", "8")
    with col3:
        st.metric("📅 Réservations aujourd'hui", "3")