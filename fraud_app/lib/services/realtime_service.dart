import 'package:flutter/foundation.dart';

class RealtimeService {
  static final ValueNotifier<int> refreshNotifier =
      ValueNotifier<int>(0);

  static void notifyUpdate() {
    refreshNotifier.value++;
  }
}