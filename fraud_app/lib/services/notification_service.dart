import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';

class NotificationService {
  static final FirebaseMessaging _messaging =
      FirebaseMessaging.instance;

  // 🔥 INITIAL SETUP
  static Future<void> initialize() async {
    // Request permission
    NotificationSettings settings =
        await _messaging.requestPermission();

    print("🔔 Permission: ${settings.authorizationStatus}");

    // Get token
    String? token = await _messaging.getToken();
    print("🔥 FCM TOKEN: $token");

    // 🔔 Foreground listener
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print("📩 Foreground message: ${message.notification?.title}");
    });

    // 🔔 When app opened from notification
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print("📲 Notification clicked");
    });
  }

  // 🔥 GET TOKEN (for backend)
  static Future<String?> getToken() async {
    return await _messaging.getToken();
  }

  // 🔥 OPTIONAL: HANDLE BACKGROUND
  static Future<void> backgroundHandler(RemoteMessage message) async {
    print("📩 Background message: ${message.notification?.title}");
  }
}