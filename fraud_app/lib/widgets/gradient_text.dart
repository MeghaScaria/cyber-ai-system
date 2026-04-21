import 'package:flutter/material.dart';

class GradientText extends StatelessWidget {
  final String text;
  final double fontSize;
  final FontWeight fontWeight;
  final Gradient gradient;

  const GradientText({
    super.key,
    required this.text,
    this.fontSize = 20,
    this.fontWeight = FontWeight.bold,
    this.gradient = const LinearGradient(
      colors: [
        Color(0xFF4C3EEB),
        Color(0xFF5B8CFF),
      ],
    ),
  });

  @override
  Widget build(BuildContext context) {
    return ShaderMask(
      shaderCallback: (bounds) {
        return gradient.createShader(
          Rect.fromLTWH(0, 0, bounds.width, bounds.height),
        );
      },
      child: Text(
        text,
        style: TextStyle(
          color: Colors.white, // required for shader
          fontSize: fontSize,
          fontWeight: fontWeight,
        ),
      ),
    );
  }
}