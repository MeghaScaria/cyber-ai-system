import 'package:flutter/material.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:fraud_ai_shield_app/services/api_service.dart';
import 'package:fraud_ai_shield_app/widgets/input_field.dart';
import 'package:fraud_ai_shield_app/widgets/premium_button.dart';
import 'package:fraud_ai_shield_app/widgets/animated_background.dart';
import 'package:fraud_ai_shield_app/widgets/gradient_text.dart';
import 'package:fraud_ai_shield_app/widgets/score_meter.dart';
import 'package:fraud_ai_shield_app/widgets/premium_glass_card.dart';

// 🔥 ADDED YOUR HISTORY IMPORTS HERE
import 'package:fraud_ai_shield_app/services/history_service.dart';
import 'package:fraud_ai_shield_app/models/history_model.dart';

class AnalyzeScreen extends StatefulWidget {
  const AnalyzeScreen({super.key});

  @override
  State<AnalyzeScreen> createState() => _AnalyzeScreenState();
}

class _AnalyzeScreenState extends State<AnalyzeScreen> {
  bool _isLoading = false;

  String result = "";
  double fraudScore = 0;

  final TextEditingController messageController = TextEditingController();

  @override
  void initState() {
    super.initState();

    // 🔥 Refresh UI when typing
    messageController.addListener(() {
      setState(() {});
    });

    // 🔔 Firebase notification popup
    FirebaseMessaging.onMessage.listen((message) {
      if (!mounted) return;

      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: Text(message.notification?.title ?? "Alert"),
          content: Text(message.notification?.body ?? "New message"),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("OK"),
            )
          ],
        ),
      );
    });
  }

  @override
  void dispose() {
    messageController.dispose();
    super.dispose();
  }

  // 🔥 API CALL
  Future<void> analyzeMessage() async {
    if (messageController.text.trim().isEmpty) return;

    setState(() {
      _isLoading = true;
      result = "";
      fraudScore = 0;
    });

    final analysis =
        await ApiService.analyzeMessage(messageController.text);

    if (analysis != null) {
      setState(() {
        result = analysis.riskLevel;
        fraudScore = analysis.fraudScore;
      });

      // 🔥 SAVE HISTORY ADDED HERE
      await HistoryService.saveHistory(
        HistoryModel(
          message: messageController.text,
          score: fraudScore, // Passing the double score directly
          result: result,
          time: DateTime.now().toString(),
        ),
      );
    } else {
      setState(() {
        result = "Server error";
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,

      body: AnimatedBackground(
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16),

            child: Column(
              children: [
                _buildHeader(),
                const SizedBox(height: 16),

                _buildInputCard(),
                const SizedBox(height: 16),

                _buildButton(),
                const SizedBox(height: 16),

                _buildResultCard(),
                const SizedBox(height: 16),

                // 🔥 SCORE METER
                ScoreMeter(score: fraudScore),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // 🔹 HEADER
  Widget _buildHeader() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Icon(Icons.security, color: Colors.white, size: 28),
        const SizedBox(width: 8),

        // ❌ removed const here
        GradientText(
          text: "Fraud Detection",
          fontSize: 24,
        ),
      ],
    );
  }

  // 🔹 INPUT CARD
  Widget _buildInputCard() {
    return _card(
      Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Enter Message", style: TextStyle(color: Colors.white)),
          const SizedBox(height: 8),

          AppInputField(
            controller: messageController,
            hint: "Enter suspicious message...",
            maxLines: 3,
            icon: Icons.message,
          ),
        ],
      ),
    );
  }

  // 🔹 BUTTON
  Widget _buildButton() {
    return PremiumButton(
      text: "START ANALYSIS",
      isLoading: _isLoading,
      onPressed: _isLoading || messageController.text.trim().isEmpty
          ? () {} // Do nothing if loading or empty
          : analyzeMessage,
    );
  }

  // 🔹 RESULT CARD
  Widget _buildResultCard() {
    bool isFraud = result.toLowerCase().contains("fraud");

    return _card(
      Column(
        children: [
          const Text("Result", style: TextStyle(color: Colors.white)),
          const SizedBox(height: 8),

          Text(
            result.isEmpty ? "Awaiting input" : result.toUpperCase(),
            style: TextStyle(
              color: isFraud ? Colors.redAccent : Colors.greenAccent,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  // 🔹 GLASS CARD WRAPPER
  Widget _card(Widget child) {
    return PremiumGlassCard(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: child,
      ),
    );
  }
}