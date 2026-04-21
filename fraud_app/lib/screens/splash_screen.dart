import 'dart:async';
import 'package:flutter/material.dart';
import 'main_navigation.dart';

import 'package:fraud_ai_shield_app/utils/page_transition.dart'; // 🔥 NEW IMPORT ADDED

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();

    Timer(const Duration(seconds: 2), () {
      // 🔥 REPLACED BULKY ROUTER WITH CUSTOM FADE TRANSITION
      Navigator.pushReplacement(
        context,
        PageTransition.fade(const MainNavigation()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF4C3EEB), Color(0xFF12141D)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),

        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.security, size: 80, color: Colors.white),
              SizedBox(height: 20),

              Text(
                "Fraud AI Shield",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              ),

              SizedBox(height: 10),

              CircularProgressIndicator(color: Colors.white),
            ],
          ),
        ),
      ),
    );
  }
}