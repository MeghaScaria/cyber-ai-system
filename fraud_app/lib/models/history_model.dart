class HistoryModel {

  final String message;
  final double score;
  final String result;
  final String time;

  HistoryModel({
    required this.message,
    required this.score,
    required this.result,
    required this.time,
  });

  // 🔥 FROM FASTAPI BACKEND
  factory HistoryModel.fromBackendJson(Map<String, dynamic> json) {

    return HistoryModel(

      message: json["content"] ?? "",

      score: (json["fraud_score"] ?? 0).toDouble(),

      result: json["risk"] ?? "unknown",

      time: json["timestamp"] ?? "",

    );
  }
}