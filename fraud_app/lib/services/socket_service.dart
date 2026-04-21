import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

class SocketService {
  static WebSocketChannel? _channel;

  // 🔥 CONNECT TO WEBSOCKET
  static void connect(Function(Map<String, dynamic>) onMessage) {
    try {
      _channel = WebSocketChannel.connect(
        Uri.parse("ws://192.168.0.189:8000/ws"), // ✅ your IP
      );

      print("✅ WebSocket connected");

      _channel!.stream.listen(
        (message) {
          print("📩 Received: $message");

          final data = jsonDecode(message);
          onMessage(data);
        },
        onError: (error) {
          print("❌ Socket Error: $error");
        },
        onDone: () {
          print("🔌 Socket Disconnected");
        },
      );
    } catch (e) {
      print("❌ Connection Failed: $e");
    }
  }

  // 🔥 SEND DATA (optional)
  static void send(Map<String, dynamic> data) {
    if (_channel != null) {
      _channel!.sink.add(jsonEncode(data));
    }
  }

  // 🔥 DISCONNECT
  static void disconnect() {
    _channel?.sink.close();
    _channel = null;
    print("🔌 Socket Closed");
  }
}