import 'package:flutter/material.dart';

class AppInputField extends StatelessWidget {
  final TextEditingController controller;
  final String hint;
  final bool isPassword;
  final int maxLines;
  final IconData? icon;

  const AppInputField({
    super.key,
    required this.controller,
    required this.hint,
    this.isPassword = false,
    this.maxLines = 1,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return TextField(
      controller: controller,
      obscureText: isPassword,
      maxLines: isPassword ? 1 : maxLines,
      style: theme.textTheme.bodyMedium,

      decoration: InputDecoration(
        hintText: hint,
        hintStyle: theme.textTheme.bodySmall,

        prefixIcon: icon != null
            ? Icon(icon, color: theme.primaryColor)
            : null,

        filled: true,
        fillColor: theme.cardColor,

        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 14),

        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }
}