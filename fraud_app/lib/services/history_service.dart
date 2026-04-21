import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/history_model.dart';

class HistoryService {
  static const String key = "fraud_history";

  // 🔥 SAVE
  static Future<void> saveHistory(HistoryModel item) async {
    final prefs = await SharedPreferences.getInstance();

    List<String> history = prefs.getStringList(key) ?? [];

    history.add(jsonEncode(item.toJson()));

    await prefs.setStringList(key, history);
  }

  // 🔥 GET ALL
  static Future<List<HistoryModel>> getHistory() async {
    final prefs = await SharedPreferences.getInstance();

    List<String> history = prefs.getStringList(key) ?? [];

    return history
        .map((item) => HistoryModel.fromJson(jsonDecode(item)))
        .toList()
        .reversed
        .toList(); // latest first
  }

  // 🔥 CLEAR (optional)
  static Future<void> clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(key);
  }
}