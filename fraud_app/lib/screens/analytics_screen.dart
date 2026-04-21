import 'package:flutter/material.dart';
import 'package:fraud_ai_shield_app/services/socket_service.dart';
import 'package:fraud_ai_shield_app/services/history_service.dart';
import 'package:fraud_ai_shield_app/models/history_model.dart';
import 'package:fraud_ai_shield_app/widgets/animated_background.dart';
import 'package:fraud_ai_shield_app/widgets/premium_glass_card.dart';
import 'package:fraud_ai_shield_app/widgets/fraud_chart.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  List<double> fraudData = [];
  int totalScans = 0;
  int fraudCount = 0;

  @override
  void initState() {
    super.initState();
    loadAnalytics();

    // 🔥 realtime socket update
    SocketService.connect((data) {
      if (!mounted) return;

      final score = (data["fraud_score"] ?? 0).toDouble();

      setState(() {
        fraudData.add(score);

        if (fraudData.length > 10) {
          fraudData.removeAt(0);
        }

        totalScans++;
        if (score > 70) fraudCount++;
      });
    });
  }

  Future<void> loadAnalytics() async {
    final history = await HistoryService.getHistory();

    setState(() {
      totalScans = history.length;

      fraudCount = history.where((item) => item.score > 70).length;

      fraudData = history
          .map((e) => e.score)
          .toList()
          .reversed
          .take(10)
          .toList()
          .reversed
          .toList();
    });
  }

  @override
  void dispose() {
    SocketService.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,

      body: AnimatedBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),

            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildHeader(),

                  const SizedBox(height: 16),

                  _buildChartCard(),

                  const SizedBox(height: 16),

                  _buildStatsRow(),

                  const SizedBox(height: 16),

                  _buildLogs(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  // 🔹 HEADER
  Widget _buildHeader() {
    return const Text(
      "Analytics",
      style: TextStyle(
        color: Colors.white,
        fontSize: 22,
        fontWeight: FontWeight.bold,
      ),
    );
  }

  // 🔹 CHART
  Widget _buildChartCard() {
    return PremiumGlassCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            "Fraud Trends",
            style: TextStyle(color: Colors.white),
          ),

          const SizedBox(height: 8),

          fraudData.isEmpty
              ? const Text(
                  "No data yet",
                  style: TextStyle(color: Colors.white54),
                )
              : FraudChart(data: fraudData),
        ],
      ),
    );
  }

  // 🔹 STATS
  Widget _buildStatsRow() {
    return Row(
      children: [
        Expanded(child: _statCard("Total Scans", totalScans.toString())),

        const SizedBox(width: 12),

        Expanded(child: _statCard("Frauds", fraudCount.toString())),
      ],
    );
  }

  Widget _statCard(String title, String value) {
    return PremiumGlassCard(
      child: Column(
        children: [
          Text(
            value,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 8),

          Text(
            title,
            style: const TextStyle(
              color: Colors.white54,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }

  // 🔹 RECENT LOGS
  Widget _buildLogs() {
    return FutureBuilder<List<HistoryModel>>(
      future: HistoryService.getHistory(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Text(
            "Loading...",
            style: TextStyle(color: Colors.white),
          );
        }

        final history = snapshot.data!.take(5).toList();

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Recent Activity",
              style: TextStyle(color: Colors.white),
            ),

            const SizedBox(height: 8),

            ...history.map((item) => _logItem(
                  item.message,
                  item.score > 70,
                )),
          ],
        );
      },
    );
  }

  Widget _logItem(String text, bool fraud) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: PremiumGlassCard(
        child: Row(
          children: [
            Icon(
              fraud ? Icons.warning : Icons.check_circle,
              color: fraud ? Colors.redAccent : Colors.greenAccent,
            ),

            const SizedBox(width: 12),

            Expanded(
              child: Text(
                text,
                style: const TextStyle(color: Colors.white),
              ),
            ),
          ],
        ),
      ),
    );
  }
}