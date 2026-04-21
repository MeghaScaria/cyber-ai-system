import smtplib
from email.mime.text import MIMEText

def send_email_alert(message, user_email="your_email@gmail.com"):
    sender_email = "your_email@gmail.com"
    app_password = "your_app_password"  # 🔥 use Gmail App Password

    subject = "🚨 Fraud Alert Detected!"
    body = f"Suspicious message detected:\n\n{message}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = user_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()

        print("📧 Email alert sent!")
    except Exception as e:
        print("Email error:", e)