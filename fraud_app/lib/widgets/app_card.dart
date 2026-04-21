import 'package:flutter/material.dart';

class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;
  final double borderRadius;

  const AppCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(16),
    this.borderRadius = 12,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      width: double.infinity,
      padding: padding,

      // 🔥 THEME-BASED COLOR
      decoration: BoxDecoration(
        color: theme.cardColor,
        borderRadius: BorderRadius.circular(borderRadius),

        // Optional subtle border for glass feel
        border: Border.all(color: Colors.white12),
      ),

      child: child,
    );
  }
}