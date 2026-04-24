def generate_explanation(risk, reasons):

    if risk == "fraud-high":
        base = "🚨 This appears to be a high-risk fraud or phishing attempt."
    elif risk == "suspicious":
        base = "⚠ This looks suspicious. Please verify before proceeding."
    else:
        base = "✅ This appears to be safe."

    if reasons:
        details = " Reasons: " + ", ".join(reasons)
    else:
        details = ""

    return base + details