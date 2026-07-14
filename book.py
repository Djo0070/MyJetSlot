import streamlit as st
from db import create_booking
import random
import datetime as dt

def show():
    st.markdown("<h1 style='text-align: center;'>✈️ Réserver un créneau</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #90CAF9;'>Choisissez votre destination et réservez en un clic</p>", unsafe_allow_html=True)
    
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("🔐 Veuillez vous connecter pour réserver.")
        return
    
    # Afficher l'ID pour debug
    user_id = st.session_state.user.get('localId')
    st.caption(f"🆔 Connecté: {user_id[:8]}...")
    
    # LISTE COMPLÈTE DES AÉROPORTS (tout est là)
    airports = {
        "🇪🇺 Europe": [
            "Nice Côte d'Azur (NCE) - France",
            "Paris Le Bourget (LBG) - France",
            "Cannes-Mandelieu (CEQ) - France",
            "Monaco Héliport (MCM) - Monaco",
            "Genève (GVA) - Suisse",
            "Milan Linate (LIN) - Italie",
            "Rome Ciampino (CIA) - Italie",
            "London Biggin Hill (BQH) - Royaume-Uni",
            "Farnborough (FAB) - Royaume-Uni",
            "Barcelone (BCN) - Espagne",
            "Palma de Majorque (PMI) - Espagne",
            "Cascais (CAT) - Portugal",
            "Munich (MUC) - Allemagne",
            "Vienne (VIE) - Autriche"
        ],
        "🌍 Moyen-Orient & Asie": [
            "Dubaï Al Maktoum (DWC) - Émirats Arabes Unis",
            "Dubaï International (DXB) - Émirats Arabes Unis",
            "Doha Hamad (DOH) - Qatar",
            "Riyad (RUH) - Arabie Saoudite",
            "Singapour Changi (SIN) - Singapour",
            "Tokyo Narita (NRT) - Japon"
        ],
        "🌎 Amérique": [
            "Teterboro (TEB) - New York, USA",
            "Van Nuys (VNY) - Los Angeles, USA",
            "Miami Opa-Locka (OPF) - Miami, USA",
            "Palm Beach (PBI) - Floride, USA",
            "Toronto Buttonville (YKZ) - Canada",
            "Mexico City (MEX) - Mexique"
        ],
        "🌍 Afrique": [
            "Le Cap (CPT) - Afrique du Sud",
            "Marrakech (RAK) - Maroc",
            "Nairobi Wilson (WIL) - Kenya"
        ]
    }
    
    ports = {
        "🇪🇺 Europe": [
            "Port de Monaco - Monaco",
            "Port de Cannes - France",
            "Port de Saint-Tropez - France",
            "Port de Marseille - France",
            "Port de Nice - France",
            "Porto Cervo - Sardaigne, Italie",
            "Port de Capri - Italie",
            "Port Hercule - Monaco",
            "Port de Barcelone - Espagne",
            "Port de Palma - Majorque, Espagne",
            "Port de Mykonos - Grèce",
            "Port de Santorin - Grèce",
            "Port de Split - Croatie",
            "Port de Bodrum - Turquie"
        ],
        "🌎 Amérique": [
            "Miami Marina - Floride, USA",
            "Newport Harbor - Californie, USA",
            "Marina del Rey - Los Angeles, USA",
            "Nassau Marina - Bahamas",
            "Tortola Marina - Îles Vierges Britanniques",
            "George Town - Grand Cayman"
        ],
        "🌍 Asie & Océanie": [
            "ONE°15 Marina - Singapour",
            "Royal Phuket Marina - Thaïlande",
            "Dubaï Marina - Émirats Arabes Unis",
            "Sydney Harbour - Australie"
        ]
    }
    
    # Type de transport
    booking_type = st.radio(
        "✈️ Type de transport",
        ["✈️ Aviation (Jet)", "🚢 Maritime (Yacht)"],
        horizontal=True
    )
    
    st.divider()
    
    if booking_type == "✈️ Aviation (Jet)":
        region = st.selectbox("🌍 Région", list(airports.keys()))
        location = st.selectbox("📍 Aéroport", airports[region])
    else:
        region = st.selectbox("🌍 Région", list(ports.keys()))
        location = st.selectbox("📍 Port", ports[region])
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("📅 Date", dt.date.today())
    with col2:
        time = st.time_input("⏰ Heure", dt.time(10, 0))
    
    duration = st.slider("⏱️ Durée (minutes)", 30, 180, 60, 15)
    
    st.divider()
    
    st.markdown("### 📋 Récapitulatif")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Type :** {booking_type}")
    with col2:
        st.markdown(f"**Lieu :** {location}")
    with col3:
        st.markdown(f"**Date :** {date.strftime('%d/%m/%Y')} à {time.strftime('%H:%M')}")
    
    if st.button("📅 Réserver maintenant", type="primary", use_container_width=True):
        booking_id = create_booking(
            st.session_state.user['localId'],
            booking_type,
            location,
            date.isoformat(),
            time.strftime("%H:%M"),
            duration
        )
        
        if booking_id:
            st.balloons()
            st.success(f"✅ Réservation #{booking_id} confirmée !")
            st.rerun()
        else:
            st.error("❌ Erreur lors de la réservation")