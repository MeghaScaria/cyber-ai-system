from app.services.firebase_service import send_push_notification

# 🔥 replace with your real token later
test_token = "YOUR_DEVICE_TOKEN"

send_push_notification(test_token, "🔥 Test Notification from AI System")