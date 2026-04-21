import 'package:flutter/material.dart';
import 'package:fraud_ai_shield_app/services/history_service.dart';
import 'package:fraud_ai_shield_app/models/history_model.dart';
import 'package:fraud_ai_shield_app/widgets/animated_background.dart';
import 'package:fraud_ai_shield_app/widgets/premium_glass_card.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<HistoryModel> historyList = [];

  @override
  void initState() {
    super.initState();
    loadHistory();
  }

  Future<void> loadHistory() async {
    final data = await HistoryService.getHistory(); // ✅ FIXED
    setState(() {
      historyList = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,

      body: AnimatedBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),

            child: Column(
              children: [
                _buildHeader(),
                const SizedBox(height: 16),

                Expanded(
                  child: historyList.isEmpty
                      ? _emptyState()
                      : ListView.builder(
                          itemCount: historyList.length,
                          itemBuilder: (context, index) {
                            final item = historyList[index];
                            return _historyCard(context, item);
                          },
                        ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // 🔹 HEADER
  Widget _buildHeader() {
    return const Text(
      "History",
      style: TextStyle(
        color: Colors.white,
        fontSize: 22,
        fontWeight: FontWeight.bold,
      ),
    );
  }

  // 🔹 EMPTY STATE
  Widget _emptyState() {
    return const Center(
      child: Text(
        "No history yet",
        style: TextStyle(color: Colors.white54),
      ),
    );
  }

  // 🔹 HISTORY CARD
  Widget _historyCard(BuildContext context, HistoryModel item) {
    bool isFraud = item.result.toLowerCase().contains("fraud");

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),

      // 🔥 UPGRADED TO GLASS CARD
      child: PremiumGlassCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              item.message,
              style: const TextStyle(color: Colors.white),
            ),

            const SizedBox(height: 8),

            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  item.result.toUpperCase(),
                  style: TextStyle(
                    color: isFraud ? Colors.redAccent : Colors.greenAccent,
                    fontWeight: FontWeight.bold,
                  ),
                ),

                Text(
                  "${item.score.toInt()}%",
                  style: TextStyle(
                    color: isFraud ? Colors.redAccent : Colors.greenAccent,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 6),

            Text(
              item.time,
              style: const TextStyle(
                color: Colors.white54,
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }
}