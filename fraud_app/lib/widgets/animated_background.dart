import 'dart:ui';
import 'package:flutter/material.dart';

class AnimatedBackground extends StatefulWidget {
  final Widget child;

  const AnimatedBackground({super.key, required this.child});

  @override
  State<AnimatedBackground> createState() => _AnimatedBackgroundState();
}

class _AnimatedBackgroundState extends State<AnimatedBackground>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 12),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return AnimatedBuilder(
      animation: _controller,
      builder: (_, __) {
        final t = _controller.value;

        return Stack(
          children: [
            // 🔥 Base background (theme)
            Container(
              decoration: BoxDecoration(
                color: theme.scaffoldBackgroundColor,
              ),
            ),

            // 🔵 Moving blob 1
            _blob(
              size: 260,
              color: Colors.blueAccent,
              top: -80 + 120 * t,
              left: -60 + 80 * (1 - t),
            ),

            // 🟣 Moving blob 2
            _blob(
              size: 300,
              color: Colors.purpleAccent,
              top: 200 + 80 * (1 - t),
              right: -80 + 60 * t,
            ),

            // 🟢 Moving blob 3
            _blob(
              size: 240,
              color: Colors.tealAccent,
              bottom: -100 + 120 * t,
              left: -40 + 100 * t,
            ),

            // 🌫 Blur overlay (Figma feel)
            BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 60, sigmaY: 60),
              child: Container(color: Colors.transparent),
            ),

            // 🔥 Foreground content
            widget.child,
          ],
        );
      },
    );
  }

  // 🔹 Blob widget
  Widget _blob({
    required double size,
    required Color color,
    double? top,
    double? left,
    double? right,
    double? bottom,
  }) {
    return Positioned(
      top: top,
      left: left,
      right: right,
      bottom: bottom,
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: RadialGradient(
            colors: [
              color.withOpacity(0.7),
              color.withOpacity(0.2),
              Colors.transparent,
            ],
          ),
        ),
      ),
    );
  }
}