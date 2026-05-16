import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/history_model.dart';

class HistoryService {

  // 🔥 CHANGE THIS TO YOUR CURRENT BACKEND IP
  static const String baseUrl = "http://10.166.204.223:8000";

  // 🔥 FETCH HISTORY FROM FASTAPI
  static Future<List<HistoryModel>> getHistory() async {

    try {

      final response = await http.get(
        Uri.parse("$baseUrl/history/guest_user"),
      );

      if (response.statusCode == 200) {

        final data = jsonDecode(response.body);

        final List history = data["history"];

        return history
            .map((item) => HistoryModel.fromBackendJson(item))
            .toList();

      } else {

        print("❌ Failed to load history");
        return [];

      }

    } catch (e) {

      print("❌ History Exception: $e");
      return [];

    }
  }
}