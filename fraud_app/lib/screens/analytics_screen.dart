import 'package:flutter/material.dart';
import 'package:fraud_ai_shield_app/services/socket_service.dart';
import 'package:fraud_ai_shield_app/services/history_service.dart';
import 'package:fraud_ai_shield_app/models/history_model.dart';
import 'package:fraud_ai_shield_app/widgets/animated_background.dart';
import 'package:fraud_ai_shield_app/widgets/premium_glass_card.dart';
import 'package:fraud_ai_shield_app/widgets/fraud_chart.dart';
import 'package:fraud_ai_shield_app/services/realtime_service.dart';

class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  List<double> fraudData = [];
  int totalScans = 0;
  int fraudCount = 0;
  double detectionRate = 0;
  @override
  @override
void initState() {
  super.initState();

  loadAnalytics();

  RealtimeService.refreshNotifier.addListener(() {
    if (mounted) {
      loadAnalytics();
    }
  });
}

  Future<void> loadAnalytics() async {
    final history = await HistoryService.getHistory();

    setState(() {
      totalScans = history.length;

      fraudCount = history.where((item) => item.score > 70).length;
      detectionRate = totalScans == 0
        ? 0
        : (fraudCount / totalScans) * 100;

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

  return Column(
    children: [

      Row(
        children: [

          Expanded(
            child: _statCard(
              "Total Scans",
              totalScans.toString(),
            ),
          ),

          const SizedBox(width: 12),

          Expanded(
            child: _statCard(
              "Frauds",
              fraudCount.toString(),
            ),
          ),

        ],
      ),

      const SizedBox(height: 12),

      _wideStatCard(
        "Detection Rate",
        "${detectionRate.toStringAsFixed(1)}%",
      ),
      

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

  Widget _wideStatCard(String title, String value) {

  return PremiumGlassCard(
    child: Column(
      children: [

        Text(
          value,
          style: const TextStyle(
            color: Colors.orangeAccent,
            fontSize: 28,
            fontWeight: FontWeight.bold,
          ),
        ),

        const SizedBox(height: 8),

        Text(
          title,
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 14,
          ),
        ),

      ],
    ),
  );
  }

  Color _severityColor(double score) {

  if (score >= 70) {
    return Colors.redAccent;
  }

  if (score >= 40) {
    return Colors.orangeAccent;
  }

  return Colors.greenAccent;
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
              "Live Threat Feed",
              style: TextStyle(color: Colors.white),
            ),

            const SizedBox(height: 8),

            ...history.map((item) => _logItem(item)),
          ],
        );
      },
    );
  }

  Widget _logItem(HistoryModel item) {

  final Color severityColor =
      _severityColor(item.score);

  final String severityLabel =
      item.score >= 70
          ? "HIGH RISK"
          : item.score >= 40
              ? "SUSPICIOUS"
              : "SAFE";

  return Padding(
    padding: const EdgeInsets.only(bottom: 12),

    child: PremiumGlassCard(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [

          Icon(
            item.score >= 70
                ? Icons.warning
                : item.score >= 40
                    ? Icons.error_outline
                    : Icons.check_circle,

            color: severityColor,
            size: 28,
          ),

          const SizedBox(width: 12),

          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,

              children: [

                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 10,
                    vertical: 4,
                  ),

                  decoration: BoxDecoration(
                    color: severityColor.withOpacity(0.15),

                    borderRadius:
                        BorderRadius.circular(8),
                  ),

                  child: Text(
                    severityLabel,

                    style: TextStyle(
                      color: severityColor,
                      fontWeight: FontWeight.bold,
                      fontSize: 11,
                    ),
                  ),
                ),

                const SizedBox(height: 8),

                Text(
                  item.message,

                  style: const TextStyle(
                    color: Colors.white,
                  ),
                ),

                const SizedBox(height: 6),

                Text(
                  "${item.score.toInt()}% risk",

                  style: TextStyle(
                    color: severityColor,
                    fontSize: 12,
                  ),
                ),

              ],
            ),
          ),
        ],
      ),
    ),
  );
  }
}