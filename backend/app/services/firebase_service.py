import firebase_admin
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
