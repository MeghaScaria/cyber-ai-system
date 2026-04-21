import 'package:flutter/material.dart';
import 'package:fraud_ai_shield_app/widgets/animated_background.dart';
import 'package:fraud_ai_shield_app/widgets/typewriter_text.dart';

class FutureScreen extends StatelessWidget {
  const FutureScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: Colors.transparent,

      body: AnimatedBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16),

            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildHeader(),

                // 🔥 SECTION GAP
                const SizedBox(height: 24),

                Expanded(
                  child: ListView(
                    children: [
                      _featureCard(
                        theme,
                        icon: Icons.psychology,
                        title: "AI Upgrade",
                        desc: "BERT / Transformer-based fraud detection",
                      ),

                      const SizedBox(height: 16),

                      _featureCard(
                        theme,
                        icon: Icons.sms,
                        title: "Real-time Protection",
                        desc: "Automatic SMS and phishing detection",
                      ),

                      const SizedBox(height: 16),

                      _featureCard(
                        theme,
                        icon: Icons.analytics,
                        title: "Analytics & Insights",
                        desc: "Fraud trends and user behavior tracking",
                      ),

                      const SizedBox(height: 16),

                      _featureCard(
                        theme,
                        icon: Icons.security,
                        title: "Security Expansion",
                        desc: "Multi-platform protection system",
                      ),

                      const SizedBox(height: 16),

                      _featureCard(
                        theme,
                        icon: Icons.rocket_launch,
                        title: "Vision",
                        desc: "Building an AI-powered cyber security assistant",
                      ),

                      // 🔥 BIG GAP BEFORE QUOTE
                      const SizedBox(height: 32),

                      _quote(),

                      const SizedBox(height: 16),
                    ],
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
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: const [
        TypewriterText(
          text: "AI-Powered Fraud Detection System 🚀",
          speed: Duration(milliseconds: 30),
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),

        SizedBox(height: 8),

        Text(
          "Predict. Detect. Protect.",
          style: TextStyle(
            fontStyle: FontStyle.italic,
            color: Colors.white70,
          ),
        ),
      ],
    );
  }

  // 🔹 FEATURE CARD
  Widget _featureCard(
    ThemeData theme, {
    required IconData icon,
    required String title,
    required String desc,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),

      decoration: BoxDecoration(
        color: theme.cardColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white24),
      ),

      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: theme.primaryColor.withOpacity(0.2),
            ),
            child: Icon(icon, color: theme.primaryColor),
          ),

          const SizedBox(width: 16),

          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),

                const SizedBox(height: 4),

                Text(
                  desc,
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: Colors.white70,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // 🔹 QUOTE
  Widget _quote() {
    return const Center(
      child: TypewriterText(
        text: "Securing tomorrow, today.",
        speed: Duration(milliseconds: 40),
        style: TextStyle(
          fontSize: 18,
          fontStyle: FontStyle.italic,
          color: Colors.white70,
        ),
      ),
    );
  }
}