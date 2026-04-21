import firebase_admin
from firebase_admin import credentials, messaging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.abspath(os.path.join(BASE_DIR, "..", "firebase_key.json"))

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


def send_push_notification(token, message_text):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title="🚨 Fraud Alert",
                body=message_text
            ),
            token=token,
        )

        response = messaging.send(message)
        print("✅ Push sent:", response)

        return response

    except Exception as e:
        print("❌ Firebase error:", str(e))
        return None