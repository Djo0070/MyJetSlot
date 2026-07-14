import streamlit as st
import sys
import os

# Ajouter le dossier courant au chemin
sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="JetSlot - Réservation Privée",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger le CSS
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Initialisation de session
if "user" not in st.session_state:
    st.session_state.user = None

# ============================================
# IMPORT DES PAGES (AVEC sys.path)
# ============================================
# Ajouter le dossier pages au chemin
sys.path.append(os.path.join(os.path.dirname(__file__), "pages"))

# Importer chaque page
import dashboard
import book
import history
import profile
import signup

# ============================================
# LOGO JETSLOT (dans la sidebar)
# ============================================
logo_svg = '''
<svg width="200" height="80" viewBox="0 0 200 80" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="gradGold" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#FFD700"/>
            <stop offset="100%" stop-color="#F4A460"/>
        </linearGradient>
        <linearGradient id="gradBlue" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1A2A4A"/>
            <stop offset="100%" stop-color="#0A1628"/>
        </linearGradient>
    </defs>
    <rect x="0" y="0" width="200" height="80" rx="12" fill="url(#gradBlue)" stroke="#FFD700" stroke-width="1.5"/>
    <path d="M15 40 L28 40 L32 35 L45 35 L42 40 L50 40 L45 45 L32 45 L28 50 L15 50 L18 45 L12 45 L15 40Z" fill="url(#gradGold)" opacity="0.9"/>
    <path d="M55 50 L45 40 L65 40 L55 50Z" fill="#FFD700" opacity="0.7"/>
    <text x="75" y="42" font-family="'Georgia', serif" font-weight="700" font-size="22" fill="url(#gradGold)" letter-spacing="2">JetSlot</text>
    <text x="75" y="58" font-family="'Arial', sans-serif" font-weight="400" font-size="9" fill="#B8C6E0" letter-spacing="2.5">PRIVATE AVIATION & YACHT</text>
</svg>
'''

# ============================================
# SIDEBAR (avec le logo)
# ============================================
with st.sidebar:
    # Logo en haut de la sidebar
    st.markdown('<div style="display: flex; justify-content: center; padding: 10px 0 20px 0;">' + logo_svg + '</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Menu de navigation
    menu = st.radio(
        "Navigation",
        ["📊 Dashboard", "📅 Réserver", "📜 Historique", "👤 Profil", "📝 Créer un compte"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # État de connexion
    if st.session_state.user:
        st.success(f"✅ {st.session_state.user.get('email', 'Connecté')}")
        if st.button("🚪 Se déconnecter", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    else:
        st.info("🔒 Non connecté")

# ============================================
# PAGES
# ============================================
if menu == "📊 Dashboard":
    dashboard.show()
elif menu == "📅 Réserver":
    book.show()
elif menu == "📜 Historique":
    history.show()
elif menu == "👤 Profil":
    profile.show()
elif menu == "📝 Créer un compte":
    signup.show()

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6C6F78; font-size: 12px;'>JetSlot - Private Aviation & Yacht Reservation © 2026</p>", unsafe_allow_html=True)
