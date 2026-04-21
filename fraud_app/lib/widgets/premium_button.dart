import 'package:flutter/material.dart';

class PremiumButton extends StatefulWidget {
  final String text;
  final VoidCallback? onPressed; // 👈 Fixed for nullability!
  final bool isLoading;

  const PremiumButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.isLoading = false,
  });

  @override
  State<PremiumButton> createState() => _PremiumButtonState();
}

class _PremiumButtonState extends State<PremiumButton> {
  bool _isPressed = false;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return GestureDetector(
      onTapDown: (_) => setState(() => _isPressed = true),
      onTapUp: (_) => setState(() => _isPressed = false),
      onTapCancel: () => setState(() => _isPressed = false),

      onTap: widget.isLoading ? null : widget.onPressed,

      child: AnimatedContainer(
        // 🔥 UPGRADED DURATION FOR SMOOTHER ANIMATION
        duration: const Duration(milliseconds: 200),
        transform: Matrix4.identity()
          ..scale(_isPressed ? 0.96 : 1.0),

        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(14),

          // 🔥 GRADIENT
          gradient: LinearGradient(
            colors: [
              theme.primaryColor,
              theme.primaryColor.withOpacity(0.7),
            ],
          ),

          // 🔥 GLOW EFFECT
          boxShadow: [
            BoxShadow(
              color: theme.primaryColor.withOpacity(0.5),
              blurRadius: 15,
              spreadRadius: 1,
            )
          ],
        ),

        child: Container(
          alignment: Alignment.center,
          height: 55,
          width: double.infinity,

          child: widget.isLoading
              ? const CircularProgressIndicator(color: Colors.white)
              : Text(
                  widget.text,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
        ),
      ),
    );
  }
}