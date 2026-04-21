import firebase_admin
<<<<<<< Updated upstream
from firebase_admin import credentials, messaging, auth, firestore
from app.config.settings import settings

# Initialize Firebase
# if settings.FIREBASE_CREDENTIALS_PATH:
#     cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
#     firebase_admin.initialize_app(cred)

async def send_push_notification(token: str, title: str, body: str):
    """
    Sends a push notification via FCM.
    """
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token
    )
    # response = messaging.send(message)
    return {"status": "sent"}

async def verify_id_token(id_token: str):
    """
    Verifies a Firebase ID token.
    """
    # decoded_token = auth.verify_id_token(id_token)
    return {"uid": "placeholder_uid"}
=======
from firebase_admin import credentials, messaging
import os
import logging
from app.config.settings import settings

logger = logging.getLogger(__name__)

# Initialize Firebase only if credentials are provided and exist
firebase_initialized = False

def initialize_firebase():
    global firebase_initialized
    cred_path = settings.FIREBASE_CREDENTIALS_PATH
    
    if not cred_path:
        logger.warning("🔥 FIREBASE_CREDENTIALS_PATH not set in .env. Push notifications will be disabled.")
        return False
        
    if not os.path.exists(cred_path):
        logger.warning(f"🔥 Firebase credentials file not found at: {cred_path}. Push notifications will be disabled.")
        return False

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("✅ Firebase initialized successfully.")
        firebase_initialized = True
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize Firebase: {e}")
        return False

# Attempt initialization on import
initialize_firebase()

def send_push_notification(token, message_text):
    if not firebase_initialized:
        logger.warning("🔔 Skip sending notification: Firebase not initialized.")
        return None
        
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title="🚨 Fraud Alert",
                body=message_text
            ),
            token=token,
        )

        response = messaging.send(message)
        logger.info(f"✅ Push sent: {response}")
        return response

    except Exception as e:
        logger.error(f"❌ Firebase error: {e}")
        return None
>>>>>>> Stashed changes
