import 'package:flutter/material.dart';

// 🔥 YOUR IMPORTS
import 'screens/splash_screen.dart';
import 'theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,

      // ✅ APPLY THEME
      theme: AppTheme.darkTheme,

      // 🔥 START APP
      home: const SplashScreen(),
    );
  }
}