import 'package:flutter/material.dart';
import 'main_navigation.dart';

import 'package:fraud_ai_shield_app/widgets/input_field.dart';
import 'package:fraud_ai_shield_app/widgets/premium_button.dart';
import 'package:fraud_ai_shield_app/widgets/animated_background.dart';
import 'package:fraud_ai_shield_app/widgets/premium_glass_card.dart';
import 'package:fraud_ai_shield_app/utils/page_transition.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  bool isLoading = false;

  void login() async {
    if (emailController.text.isEmpty || passwordController.text.isEmpty) {
      _showError("Please fill all fields");
      return;
    }

    setState(() => isLoading = true);

    await Future.delayed(const Duration(seconds: 1));

    setState(() => isLoading = false);

    Navigator.pushReplacement(
      context,
      PageTransition.fade(const MainNavigation()),
    );
  }

  void _showError(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,

      body: AnimatedBackground(
        child: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(20),

              child: PremiumGlassCard(
                child: Padding(
                  padding: const EdgeInsets.all(20),

                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text(
                        "Welcome Back",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),

                      // 🔥 SECTION GAP
                      const SizedBox(height: 24),

                      // 🔥 EMAIL
                      AppInputField(
                        controller: emailController,
                        hint: "Email",
                        icon: Icons.email,
                      ),

                      // 🔥 FIELD GAP
                      const SizedBox(height: 16),

                      // 🔥 PASSWORD
                      AppInputField(
                        controller: passwordController,
                        hint: "Password",
                        isPassword: true,
                        icon: Icons.lock,
                      ),

                      // 🔥 SECTION GAP
                      const SizedBox(height: 24),

                      // 🔥 BUTTON
                      PremiumButton(
                        text: "Login",
                        isLoading: isLoading,
                        onPressed: login,
                      ),

                      // 🔥 SMALL GAP
                      const SizedBox(height: 16),

                      const Text(
                        "Don’t have an account? Sign up",
                        style: TextStyle(
                          color: Colors.white54,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}