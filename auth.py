import pyrebase
import os
from dotenv import load_dotenv
import streamlit as st
from google.cloud import firestore
from db import db, init_firestore

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

# Vérifier que la configuration Firebase est complète
if not all(firebase_config.values()):
    st.warning("⚠️ Configuration Firebase incomplète. Vérifie ton fichier .env")
else:
    # Initialiser Firebase Auth
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

# S'assurer que Firestore est initialisé
if db is None:
    init_firestore()

def sign_in(email, password):
    """Connecte un utilisateur avec email et mot de passe"""
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Récupérer les infos utilisateur depuis Firestore
        if db is not None:
            try:
                user_doc = db.collection("users").document(user['localId']).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    user['name'] = user_data.get('name', email.split('@')[0])
            except Exception as e:
                st.warning(f"⚠️ Impossible de récupérer les infos utilisateur : {e}")
        
        # Stocker l'utilisateur dans la session
        st.session_state.user = user
        st.success("✅ Connexion réussie !")
        return user
        
    except Exception as e:
        # Gérer les erreurs Firebase de manière plus claire
        error_msg = str(e)
        if "EMAIL_NOT_FOUND" in error_msg:
            st.error("❌ Email non trouvé")
        elif "INVALID_PASSWORD" in error_msg:
            st.error("❌ Mot de passe incorrect")
        elif "USER_DISABLED" in error_msg:
            st.error("❌ Compte désactivé")
        else:
            st.error(f"❌ Erreur de connexion : {error_msg}")
        return None

def sign_up(email, password):
    """Crée un nouvel utilisateur"""
    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        # Ajouter l'utilisateur dans Firestore
        if db is not None:
            try:
                db.collection("users").document(user['localId']).set({
                    "email": email,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "name": email.split('@')[0]  # Nom par défaut
                })
                st.success("✅ Utilisateur créé dans Firestore")
            except Exception as e:
                st.warning(f"⚠️ Erreur Firestore : {e}")
        
        # Stocker l'utilisateur dans la session
        user['name'] = email.split('@')[0]
        st.session_state.user = user
        st.success("✅ Compte créé avec succès !")
        return user
        
    except Exception as e:
        # Gérer les erreurs Firebase
        error_msg = str(e)
        if "EMAIL_EXISTS" in error_msg:
            st.error("❌ Cet email est déjà utilisé")
        elif "WEAK_PASSWORD" in error_msg:
            st.error("❌ Mot de passe trop faible (minimum 6 caractères)")
        else:
            st.error(f"❌ Erreur d'inscription : {error_msg}")
        return None

def sign_out():
    """Déconnecte l'utilisateur"""
    try:
        st.session_state.user = None
        # Nettoyer les données temporaires
        if "booking_data" in st.session_state:
            del st.session_state.booking_data
        st.success("🔒 Déconnecté avec succès")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Erreur lors de la déconnexion : {e}")

def get_user():
    """Retourne l'utilisateur connecté"""
    if "user" in st.session_state and st.session_state.user is not None:
        return st.session_state.user
    return None

def is_authenticated():
    """Vérifie si l'utilisateur est connecté"""
    return st.session_state.get("user") is not None

def get_user_id():
    """Retourne l'ID de l'utilisateur connecté"""
    user = get_user()
    if user:
        return user.get('localId')
    return None