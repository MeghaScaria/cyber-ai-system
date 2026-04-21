import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

// 🔥 YOUR IMPORTS
import 'services/notification_service.dart';
import 'screens/splash_screen.dart'; // 👈 NEW IMPORT: Splash Screen
import 'theme/app_theme.dart'; 

// ✅ BACKGROUND HANDLER
Future<void> _firebaseBackgroundHandler(RemoteMessage message) async {
  print("📩 Background message: ${message.notification?.title}");
}

// ✅ MAIN FUNCTION
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  // Listen for background messages
  FirebaseMessaging.onBackgroundMessage(_firebaseBackgroundHandler);

  // Initialize your custom notification service
  await NotificationService.initialize();

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
      
      // 🔥 UPDATED: APP NOW STARTS WITH SPLASH SCREEN
      home: const SplashScreen(), 
    );
  }
}