from app.services.sms_service import send_sms_alert

print("🚀 Starting SMS test...")

try:
    send_sms_alert(
        "🔥 Test fraud message from AI system",
        "+918431446252"   # 🔥 put your real number here
    )
    print("✅ Function executed")

except Exception as e:
    print("❌ Error occurred:", e)