import os
import json
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

# --- Initialisation de Firestore ---
db = None

def init_firestore():
    """Initialise la connexion à Firestore"""
    global db
    
    # Méthode 1 : via fichier JSON local (développement)
    cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
    if os.path.exists(cred_path):
        try:
            cred = service_account.Credentials.from_service_account_file(cred_path)
            db = firestore.Client(credentials=cred, project="aneyond-3bbc5")
            st.success("✅ Firestore connecté (fichier local)")
            return True
        except Exception as e:
            st.warning(f"Erreur Firestore (fichier) : {e}")
    
    # Méthode 2 : via variable d'environnement
    firebase_cred_str = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    if firebase_cred_str:
        try:
            firebase_cred = json.loads(firebase_cred_str)
            cred = service_account.Credentials.from_service_account_info(firebase_cred)
            db = firestore.Client(credentials=cred, project=firebase_cred["project_id"])
            st.success("✅ Firestore connecté (secret)")
            return True
        except Exception as e:
            st.warning(f"Erreur Firestore (secret) : {e}")
    
    # Si rien ne fonctionne, mode simulation
    st.warning("⚠️ Firestore non configuré. Mode simulation (données non persistantes).")
    db = None
    return False

# Initialiser au chargement
init_firestore()

# --- FONCTIONS RÉSERVATIONS ---
def get_bookings(user_id):
    """Récupère les réservations d'un utilisateur"""
    if not user_id:
        st.error("❌ user_id manquant")
        return []
    
    # Mode simulation - Données factices
    if db is None:
        st.info("🔧 Mode simulation - Réservations factices")
        return [
            {
                "id": "sim1",
                "userId": user_id,
                "type": "Aviation (Jet)",
                "location": "Nice Côte d'Azur (NCE) - France",
                "date": "2026-07-20",
                "time": "10:30",
                "duration": 60,
                "status": "confirmed"
            },
            {
                "id": "sim2",
                "userId": user_id,
                "type": "Maritime (Yacht)",
                "location": "Port de Monaco - Monaco",
                "date": "2026-07-25",
                "time": "14:00",
                "duration": 120,
                "status": "pending"
            }
        ]
    
    try:
        # Récupérer toutes les réservations de l'utilisateur
        bookings_ref = db.collection("bookings").where("userId", "==", user_id)
        bookings = bookings_ref.stream()
        
        result = []
        for b in bookings:
            data = b.to_dict()
            data["id"] = b.id
            result.append(data)
        
        # Trier par date (plus récent d'abord)
        result.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        if result:
            st.success(f"✅ {len(result)} réservation(s) trouvée(s)")
        else:
            st.info("📭 Aucune réservation trouvée dans Firestore")
        
        return result
        
    except Exception as e:
        st.error(f"❌ Erreur de récupération des réservations : {e}")
        return []

def create_booking(user_id, booking_type, location, date, time, duration=60):
    """Crée une nouvelle réservation"""
    if not user_id:
        st.error("❌ Utilisateur non connecté")
        return None
    
    # Récupérer l'email de l'utilisateur
    user_email = None
    user_name = "Client"
    
    if st.session_state.user:
        user_email = st.session_state.user.get("email")
        if user_email:
            user_name = user_email.split('@')[0]
    
    # Préparer les données
    booking_data = {
        "userId": user_id,
        "type": booking_type,
        "location": location,
        "date": date,
        "time": time,
        "duration": duration,
        "status": "pending"
    }
    
    # --- Mode simulation ---
    if db is None:
        import random
        import string
        booking_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        booking_data["id"] = booking_id
        st.info(f"🔧 [SIMULATION] Réservation créée : {booking_id}")
        
        # Envoyer email en simulation
        if user_email:
            try:
                from notifications import send_confirmation_email
                send_confirmation_email(user_email, booking_data)
            except Exception as e:
                st.warning(f"⚠️ Erreur email (simu) : {e}")
        
        return booking_id
    
    # --- Mode réel (Firestore) ---
    try:
        # Ajouter created_at seulement si Firestore est connecté
        booking_data["created_at"] = firestore.SERVER_TIMESTAMP
        
        doc_ref = db.collection("bookings").document()
        doc_ref.set(booking_data)
        booking_id = doc_ref.id
        
        st.success(f"✅ Réservation #{booking_id} sauvegardée dans Firestore")
        
        # Envoyer email de confirmation
        if user_email:
            try:
                from notifications import send_confirmation_email
                booking_data["id"] = booking_id
                booking_data["user_name"] = user_name
                send_confirmation_email(user_email, booking_data)
            except Exception as e:
                st.warning(f"⚠️ Erreur email : {e}")
        
        return booking_id
        
    except Exception as e:
        st.error(f"❌ Erreur de création dans Firestore : {e}")
        return None

def cancel_booking(booking_id, user_id):
    """Annule une réservation"""
    if not booking_id:
        st.error("❌ ID de réservation manquant")
        return False
    
    if not user_id:
        st.error("❌ Utilisateur non identifié")
        return False
    
    # Mode simulation
    if db is None:
        st.info("🔧 [SIMULATION] Annulation effectuée")
        return True
    
    try:
        # Récupérer la réservation
        booking_ref = db.collection("bookings").document(booking_id)
        booking = booking_ref.get()
        
        if not booking.exists:
            st.error(f"❌ Réservation #{booking_id} introuvable dans Firestore")
            return False
        
        booking_data = booking.to_dict()
        
        # Vérifier les permissions
        if booking_data.get("userId") != user_id:
            st.error("⛔ Vous n'êtes pas autorisé à annuler cette réservation")
            return False
        
        # Vérifier si déjà annulée
        if booking_data.get("status") == "cancelled":
            st.warning("ℹ️ Cette réservation est déjà annulée")
            return True
        
        # Annuler
        booking_ref.update({
            "status": "cancelled",
            "cancelled_at": firestore.SERVER_TIMESTAMP
        })
        
        st.success(f"✅ Réservation #{booking_id} annulée dans Firestore")
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'annulation : {e}")
        return False