import 'package:flutter/foundation.dart';

class AppConfig {
  static final String apiBaseUrl = _resolveApiBaseUrl();

  static String _resolveApiBaseUrl() {
    const fromEnv = String.fromEnvironment('API_BASE_URL', defaultValue: '');
    if (fromEnv.isNotEmpty) {
      return fromEnv;
    }

    return kIsWeb ? 'http://localhost:8000' : 'http://10.0.2.2:8000';
  }
}
