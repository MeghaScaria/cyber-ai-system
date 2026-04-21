def calculate_risk(text_result, url_result, anomaly_result):
    score = 0
    reasons = []

    # 🔹 Text analysis
    text_score = int(text_result.get("score", 0))
    is_text_fraud = text_result.get("is_fraud", False)

    # Always add base text score
    score += text_score

    # Extra boost if fraud detected
    if is_text_fraud:
        score += 40
        reasons.append("Fraudulent text pattern detected")

    # Include model reasons
    reasons.extend(text_result.get("reasons", []))

    # 🔹 URL detection
    if url_result.get("detected", False):
        score += 30
        reasons.append("Phishing URL detected")

    # 🔹 Anomaly detection
    if anomaly_result.get("anomaly", False):
        score += 20
        reasons.append("User behavior anomaly detected")

    # 🔹 Smart baseline scoring
    if score == 0:
        if len(text_result.get("reasons", [])) > 0:
            score = 20   # slight suspicion
            reasons.append("Minor suspicious indicators detected")
        else:
            score = 10   # fully safe
            reasons.append("No suspicious activity detected")

    # 🔹 Cap score
    score = min(score, 100)

    # 🔹 Risk classification
    if score >= 80:
        risk_level = "fraud-high"
        confidence = "high"
    elif score >= 50:
        risk_level = "suspicious-medium"
        confidence = "medium"
    else:
        risk_level = "safe"
        confidence = "low"

    return {
        "score": score,
        "risk_level": risk_level,
        "confidence": confidence,
        "reasons": reasons
    }