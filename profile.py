import streamlit as st
from auth import sign_out

def show():
    st.markdown("<h1 style='text-align: center;'>👤 Mon profil</h1>", unsafe_allow_html=True)
    
    if "user" not in st.session_state or st.session_state.user is None:
        st.info("💡 Connectez-vous pour accéder à votre profil personnalisé.")
        # Afficher un formulaire de connexion rapide
        with st.expander("🔑 Se connecter", expanded=True):
            email = st.text_input("Email", placeholder="votre@email.com")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            if st.button("Connexion", use_container_width=True):
                from auth import sign_in
                user = sign_in(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
        return
    
    user = st.session_state.user
    st.write(f"**Email :** {user.get('email', 'Non renseigné')}")
    st.write(f"**ID utilisateur :** {user.get('localId', 'Inconnu')}")
    
    st.markdown("---")
    st.markdown("### ✈️ Mes préférences")
    
    default_type = st.selectbox("Type de transport par défaut", ["Aviation", "Maritime"])
    if st.button("💾 Sauvegarder les préférences"):
        st.success("Préférences sauvegardées !")
    
    st.markdown("---")
    if st.button("🚪 Se déconnecter", use_container_width=True, type="primary"):
        sign_out()