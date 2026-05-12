import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/analysis_model.dart';

class ApiService {
  // 🔥 CHANGE THIS TO YOUR BACKEND IP
  static const String baseUrl = "http://10.166.204.223:8000";

  // 🚀 ANALYZE MESSAGE API
  static Future<AnalysisModel?> analyzeMessage(String message) async {
    try {
      final url = Uri.parse("$baseUrl/analyze-sms");

      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "message": message,
          "user_id": "user123",
          "metadata": {}
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return AnalysisModel.fromJson(data);
      } else {
        print("❌ API Error: ${response.statusCode}");
        return null;
      }
    } catch (e) {
      print("❌ Exception: $e");
      return null;
    }
  }
}