import os
import streamlit as st
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Template HTML pour l'email de confirmation - STYLE ORIGINAL
CONFIRMATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Confirmation</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <!-- HEADER -->
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #FFD700;">
                <h1 style="color: #FFD700; font-size: 36px; margin: 0; letter-spacing: 4px; font-family: 'Georgia', serif;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        
        <!-- CONTENT -->
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #FFD700; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Confirmation de réservation</h2>
                
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #FFD700; font-weight: bold;">Bonjour Cher client,</span>
                </p>
                
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Nous avons le plaisir de vous confirmer votre réservation <span style="color: #FFD700; font-weight: bold;">#{{ id or booking_id }}</span>. Voici les détails de votre cérémonie :
                </p>
                
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #FFD700;">
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FFD700;">📍</span> <strong>Lieu</strong> : {{ location }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FFD700;">📅</span> <strong>Date</strong> : {{ date }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FFD700;">⏰</span> <strong>Heure</strong> : {{ time }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FFD700;">⏱️</span> <strong>Durée</strong> : {{ duration }} minutes
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FFD700;">🆔</span> <strong>ID de réservation</strong> : #{{ id or booking_id }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FFD700;">📊</span> <strong>Statut</strong> : <span style="color: #4CAF50; font-weight: bold;">Confirmé</span>
                        </td>
                    </tr>
                </table>
                
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">
                    Vous pouvez gérer vos réservations depuis votre espace personnel sur JetSlot.<br>
                    Pour toute question, notre équipe est à votre disposition.
                </p>
            </td>
        </tr>
        
        <!-- FOOTER -->
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #FFD700; font-size: 15px; margin: 0; font-weight: bold; letter-spacing: 1px;">
                    <span style="color: #FFD700;">Anen Youssef</span>
                </p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0; letter-spacing: 1px;">
                    Fondateur, JetSlot
                </p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    contact@myjetslot.com | +447411201949
                </p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    <a href="www.myjetslot.com" style="color: #FFD700; text-decoration: none;">www.myjetslot.com</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Support</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Conditions</a>
                </p>
                <p style="color: #4A4F58; font-size: 11px; margin: 15px 0 0 0; letter-spacing: 0.5px;">
                    © 2026 JetSlot - Tous droits réservés
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# Template pour l'annulation - STYLE ORIGINAL
CANCELLATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Annulation</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <!-- HEADER -->
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #FF4444;">
                <h1 style="color: #FF4444; font-size: 36px; margin: 0; letter-spacing: 4px; font-family: 'Georgia', serif;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        
        <!-- CONTENT -->
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #FF4444; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Annulation de réservation</h2>
                
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #FF4444; font-weight: bold;">Bonjour Cher client,</span>
                </p>
                
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Nous vous confirmons l'annulation de votre réservation <span style="color: #FF4444; font-weight: bold;">#{{ id or booking_id }}</span>.
                </p>
                
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #FF4444;">
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FF4444;">📍</span> <strong>Lieu</strong> : {{ location }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FF4444;">📅</span> <strong>Date</strong> : {{ date }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FF4444;">⏰</span> <strong>Heure</strong> : {{ time }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;">
                            <span style="color: #FF4444;">🆔</span> <strong>ID de réservation</strong> : #{{ id or booking_id }}
                        </td>
                    </tr>
                </table>
                
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">
                    Si vous n'êtes pas à l'origine de cette annulation, contactez-nous immédiatement.<br>
                    Pour toute question, notre équipe est à votre disposition.
                </p>
            </td>
        </tr>
        
        <!-- FOOTER -->
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #FFD700; font-size: 15px; margin: 0; font-weight: bold; letter-spacing: 1px;">
                    <span style="color: #FFD700;">Aner Youssef</span>
                </p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0; letter-spacing: 1px;">
                    Fondateur, JetSlot
                </p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    contact@myjetslot.com | +447411201949
                </p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    <a href="www.myjetslot.com" style="color: #FFD700; text-decoration: none;">www.myjetslot.com</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Support</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Conditions</a>
                </p>
                <p style="color: #4A4F58; font-size: 11px; margin: 15px 0 0 0; letter-spacing: 0.5px;">
                    © 2026 JetSlot - Tous droits réservés
                </p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def send_email(to_email, subject, html_content):
    """Envoie un email avec Gmail"""
    try:
        smtp_user = os.getenv("EMAIL_SENDER")
        smtp_password = os.getenv("EMAIL_PASSWORD")
        
        if not smtp_user or not smtp_password:
            st.error("❌ EMAIL_SENDER ou EMAIL_PASSWORD non configurés dans .env")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        st.success(f"📧 Email envoyé à {to_email}")
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur d'envoi email : {e}")
        return False

def send_confirmation_email(email, booking_data):
    """Envoie un email de confirmation - Style original"""
    try:
        template = Template(CONFIRMATION_TEMPLATE)
        
        # Préparer les données
        booking_data['id'] = booking_data.get('id', booking_data.get('booking_id', ''))
        booking_data['booking_type'] = booking_data.get('booking_type', booking_data.get('type', ''))
        
        html = template.render(**booking_data)
        subject = f"JetSlot - Confirmation réservation #{booking_data['id']}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"❌ Erreur template confirmation : {e}")
        return False

def send_cancellation_email(email, booking_data):
    """Envoie un email d'annulation - Style original"""
    try:
        template = Template(CANCELLATION_TEMPLATE)
        
        # Préparer les données
        booking_data['id'] = booking_data.get('id', booking_data.get('booking_id', ''))
        booking_data['booking_type'] = booking_data.get('booking_type', booking_data.get('type', ''))
        
        html = template.render(**booking_data)
        subject = f"JetSlot - Annulation réservation #{booking_data['id']}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"❌ Erreur template annulation : {e}")
        return False