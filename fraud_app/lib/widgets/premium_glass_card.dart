import 'dart:ui';
import 'package:flutter/material.dart';

class PremiumGlassCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets padding;
  final double borderRadius;

  const PremiumGlassCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(16),
    this.borderRadius = 16,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),

      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),

        child: Container(
          width: double.infinity,
          padding: padding,

          decoration: BoxDecoration(
            // 🔥 Glass transparent layer
            color: theme.cardColor.withOpacity(0.15),

            borderRadius: BorderRadius.circular(borderRadius),

            // 🔥 Subtle border
            border: Border.all(
              color: Colors.white.withOpacity(0.2),
            ),

            // 🔥 Soft glow shadow
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.2),
                blurRadius: 20,
                spreadRadius: 2,
              )
            ],
          ),

          child: child,
        ),
      ),
    );
  }
}