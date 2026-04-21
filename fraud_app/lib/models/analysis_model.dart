class AnalysisModel {
  final bool isFraud;
  final double fraudScore;
  final bool phishingDetected;
  final bool anomalyDetected;
  final String riskLevel;
  final String confidence;
  final String explanation;
  final String? alert;
  final String timestamp;
  final List<String> reasons;

  AnalysisModel({
    required this.isFraud,
    required this.fraudScore,
    required this.phishingDetected,
    required this.anomalyDetected,
    required this.riskLevel,
    required this.confidence,
    required this.explanation,
    required this.timestamp,
    required this.reasons,
    this.alert,
  });

  // 🔥 Convert JSON → Dart Object
  factory AnalysisModel.fromJson(Map<String, dynamic> json) {
    return AnalysisModel(
      isFraud: json["is_fraud"] ?? false,
      fraudScore: (json["fraud_score"] ?? 0).toDouble(),
      phishingDetected: json["phishing_detected"] ?? false,
      anomalyDetected: json["anomaly_detected"] ?? false,
      riskLevel: json["risk_level"] ?? "unknown",
      confidence: json["confidence"] ?? "low",
      explanation: json["explanation"] ?? "",
      alert: json["alert"],
      timestamp: json["timestamp"] ?? "",
      reasons: List<String>.from(json["reasons"] ?? []),
    );
  }

  // 🔥 Convert Dart Object → JSON (optional)
  Map<String, dynamic> toJson() {
    return {
      "is_fraud": isFraud,
      "fraud_score": fraudScore,
      "phishing_detected": phishingDetected,
      "anomaly_detected": anomalyDetected,
      "risk_level": riskLevel,
      "confidence": confidence,
      "explanation": explanation,
      "alert": alert,
      "timestamp": timestamp,
      "reasons": reasons,
    };
  }
}