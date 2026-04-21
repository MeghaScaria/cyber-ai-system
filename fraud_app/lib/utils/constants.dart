class AppConstants {
  // 🔥 BASE URL (Backend)
  static const String baseUrl = "http://192.168.0.189:8000";

  // 🔥 API ENDPOINTS
  static const String analyzeEndpoint = "/analyze-message";
  static const String websocketEndpoint = "/ws";

  // 🔥 FULL URL HELPERS
  static String get analyzeUrl => "$baseUrl$analyzeEndpoint";
  static String get websocketUrl => "ws://192.168.0.189:8000$websocketEndpoint";

  // 🔥 USER (TEMP - can be replaced with auth later)
  static const String userId = "user123";

  // 🔥 APP TEXTS
  static const String appName = "Fraud AI Shield";
  static const String analyzeTitle = "Fraud Detection";
  static const String analyticsTitle = "Analytics";
  static const String historyTitle = "History";

  // 🔥 ERROR MESSAGES
  static const String errorMessage = "Something went wrong";
  static const String emptyInput = "Please enter a message";

  // 🔥 TIMEOUTS
  static const int apiTimeout = 15; // seconds
}