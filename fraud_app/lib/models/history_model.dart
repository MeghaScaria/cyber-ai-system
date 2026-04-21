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

  Map<String, dynamic> toJson() => {
        "message": message,
        "score": score,
        "result": result,
        "time": time,
      };

  factory HistoryModel.fromJson(Map<String, dynamic> json) {
    return HistoryModel(
      message: json["message"],
      score: json["score"],
      result: json["result"],
      time: json["time"],
    );
  }
}