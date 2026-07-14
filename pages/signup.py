import streamlit as st
from auth import sign_up, sign_in

def show():
    st.markdown("<h1 style='text-align: center;'>📝 Créer un compte</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("signup_form"):
                email = st.text_input("📧 Email", placeholder="votre@email.com")
                password = st.text_input("🔑 Mot de passe", type="password", placeholder="••••••••")
                confirm_password = st.text_input("🔑 Confirmer le mot de passe", type="password", placeholder="••••••••")
                
                if st.form_submit_button("🚀 Créer mon compte", use_container_width=True):
                    if password != confirm_password:
                        st.error("Les mots de passe ne correspondent pas.")
                    elif len(password) < 6:
                        st.error("Le mot de passe doit contenir au moins 6 caractères.")
                    else:
                        user = sign_up(email, password)
                        if user:
                            st.success("✅ Compte créé avec succès !")
                            # Connexion automatique
                            user = sign_in(email, password)
                            if user:
                                st.session_state.user = user
                                st.rerun()
