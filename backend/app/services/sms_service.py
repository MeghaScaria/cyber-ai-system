from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")


def send_sms_alert(message_text, to_number):
    print("📩 Sending SMS...")
    print("SID:", ACCOUNT_SID)
    print("FROM:", TWILIO_NUMBER)
    print("TO:", to_number)

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages.create(
            body=f"🚨 Fraud Alert:\n{message_text}",
            from_=TWILIO_NUMBER,
            to=to_number
        )

        print("✅ SMS sent:", message.sid)

    except Exception as e:
        print("❌ SMS error:", e)