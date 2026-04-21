def generate_explanation(risk_level, reasons):
    if risk_level.startswith("fraud"):
        return "⚠️ This message is highly likely to be a scam because: " + ", ".join(reasons)

    elif risk_level.startswith("suspicious"):
        return "⚠️ This message shows some suspicious patterns: " + ", ".join(reasons)

    elif risk_level == "safe":
        return "✅ This message appears safe. It does not contain suspicious links, urgency, or requests for sensitive information."

    else:
        return "ℹ️ Unable to determine risk level."