import 'package:flutter/foundation.dart';

class AppConfig {
  // Primary: Render production backend
  static const String renderApiBaseUrl =
      'https://vertex-ids-backend.onrender.com';

  // Fallback: Local development backend (for viva/testing if render fails)
  static const String devApiBaseUrl = 'http://10.0.2.2:8000';
  static const String webDevApiBaseUrl = 'http://localhost:8000';

  static final String apiBaseUrl = _resolveApiBaseUrl();

  static String _resolveApiBaseUrl() {
    // Check for environment override
    const fromEnv = String.fromEnvironment('API_BASE_URL', defaultValue: '');
    if (fromEnv.isNotEmpty) {
      return fromEnv;
    }

    // Use Render production by default
    // Dev fallback only if specified in environment
    const useLocalDev = String.fromEnvironment(
      'USE_LOCAL_DEV',
      defaultValue: 'false',
    );
    if (useLocalDev == 'true') {
      return kIsWeb ? webDevApiBaseUrl : devApiBaseUrl;
    }

    return renderApiBaseUrl;
  }
}