import 'package:flutter/material.dart';

class ScoreMeter extends StatelessWidget {
  final double score; // 0 - 100

  const ScoreMeter({
    super.key,
    required this.score,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    Color meterColor = _getColor(score);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),

      decoration: BoxDecoration(
        color: theme.cardColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white12),
      ),

      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "Fraud Score",
            style: theme.textTheme.bodyMedium,
          ),

          const SizedBox(height: 12),

          // 🔥 PROGRESS BAR
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: TweenAnimationBuilder<double>(
              tween: Tween(begin: 0, end: score / 100),
              duration: const Duration(milliseconds: 800),
              builder: (context, value, _) {
                return LinearProgressIndicator(
                  value: value,
                  minHeight: 12,
                  backgroundColor: Colors.grey.withOpacity(0.2),
                  valueColor: AlwaysStoppedAnimation(meterColor),
                );
              },
            ),
          ),

          const SizedBox(height: 12),

          // 🔥 SCORE TEXT
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                "${score.toInt()}%",
                style: theme.textTheme.titleLarge?.copyWith(
                  color: meterColor,
                ),
              ),

              Text(
                _getLabel(score),
                style: theme.textTheme.bodySmall?.copyWith(
                  color: meterColor,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // 🔹 COLOR LOGIC
  Color _getColor(double score) {
    if (score > 70) return Colors.red;
    if (score > 40) return Colors.orange;
    return Colors.green;
  }

  // 🔹 LABEL
  String _getLabel(double score) {
    if (score > 70) return "High Risk";
    if (score > 40) return "Medium Risk";
    return "Safe";
  }
}