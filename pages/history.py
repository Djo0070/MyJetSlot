import streamlit as st
import pandas as pd
from db import get_bookings, cancel_booking

def show():
    st.markdown("<h1 style='text-align: center;'>📜 Historique des réservations</h1>", unsafe_allow_html=True)
    
    if "user" not in st.session_state or st.session_state.user is None:
        st.info("💡 Connectez-vous pour voir votre historique.")
        return
    
    user_id = st.session_state.user.get('localId')
    if not user_id:
        st.error("❌ ID utilisateur non trouvé")
        return
    
    # Afficher l'ID pour debug
    st.caption(f"🆔 ID utilisateur: {user_id[:8]}...")
    
    bookings = get_bookings(user_id)
    
    if not bookings:
        st.info("📭 Aucune réservation trouvée.")
        return
    
    # Statistiques
    df = pd.DataFrame(bookings)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total", len(df))
    with col2:
        aviation = len(df[df['type'].str.contains("Aviation", na=False)]) if 'type' in df.columns else 0
        st.metric("✈️ Aviation", aviation)
    with col3:
        maritime = len(df[df['type'].str.contains("Maritime", na=False)]) if 'type' in df.columns else 0
        st.metric("🚢 Maritime", maritime)
    
    st.markdown("---")
    st.markdown("### 📋 Détail des réservations")
    
    for b in bookings:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"**{b.get('type', 'Type inconnu')}**")
                st.caption(f"📍 {b.get('location', 'Lieu inconnu')}")
            
            with col2:
                st.markdown(f"📅 {b.get('date', 'Date inconnue')}")
                st.caption(f"🕐 {b.get('time', 'Heure inconnue')} - {b.get('duration', 60)} min")
            
            with col3:
                status = b.get('status', 'pending')
                if status == 'confirmed':
                    st.success("✅ Confirmé")
                elif status == 'pending':
                    st.warning("⏳ En attente")
                elif status == 'cancelled':
                    st.error("❌ Annulé")
                else:
                    st.info(f"ℹ️ {status}")
            
            with col4:
                if status != 'cancelled':
                    booking_id = b.get('id')
                    if st.button("❌ Annuler", key=f"cancel_btn_{booking_id}"):
                        with st.spinner("🔄 Annulation..."):
                            success = cancel_booking(booking_id, user_id)
                            if success:
                                # Envoyer email d'annulation
                                try:
                                    from notifications import send_cancellation_email
                                    user_email = st.session_state.user.get('email')
                                    if user_email:
                                        send_cancellation_email(user_email, b)
                                except Exception as e:
                                    st.warning(f"⚠️ Email: {e}")
                                
                                st.success("✅ Réservation annulée !")
                                st.rerun()
                            else:
                                st.error("❌ Échec de l'annulation")
            
            st.divider()
