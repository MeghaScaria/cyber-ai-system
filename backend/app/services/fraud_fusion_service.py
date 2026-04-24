def combine_results(url_result=None, text_result=None, anomaly_result=None):

    score = 0
    reasons = []

    # 🔥 URL (60% weight)
    if url_result:
        score += url_result.get("fraud_score", 0) * 0.6
        if url_result.get("risk") == "fraud-high":
            reasons.append("Malicious URL detected")
        elif url_result.get("risk") == "suspicious":
            reasons.append("Suspicious URL pattern")

    # 🔥 TEXT (30% weight)
    if text_result:
        score += text_result.get("fraud_score", 0) * 0.3
        if text_result.get("is_scam"):
            reasons.append("Scam message content detected")

    # 🔥 ANOMALY (10% weight)
    if anomaly_result:
        if anomaly_result.get("anomaly"):
            score += 10
            reasons.append("Unusual user behavior detected")

    score = int(score)

    # 🎯 FINAL CLASSIFICATION
    if score >= 70:
        risk = "fraud-high"
    elif score >= 40:
        risk = "suspicious"
    else:
        risk = "safe"

    return {
        "fraud_score": score,
        "risk": risk,
        "reasons": reasons
    }