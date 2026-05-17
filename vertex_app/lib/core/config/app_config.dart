import 'package:flutter/foundation.dart';

class AppConfig {
  // Primary: Vercel production backend
  static const String vercelApiBaseUrl =
      'https://vertex-ids-srs-classification-backend.vercel.app';

  // Fallback: Local development backend (for viva/testing if Vercel fails)
  static const String devApiBaseUrl = 'http://10.0.2.2:8000';
  static const String webDevApiBaseUrl = 'http://localhost:8000';

  static final String apiBaseUrl = _resolveApiBaseUrl();

  static String _resolveApiBaseUrl() {
    // Check for environment override
    const fromEnv = String.fromEnvironment('API_BASE_URL', defaultValue: '');
    if (fromEnv.isNotEmpty) {
      return fromEnv;
    }

    // Use Vercel production by default
    // Dev fallback only if specified in environment
    const useLocalDev = String.fromEnvironment(
      'USE_LOCAL_DEV',
      defaultValue: 'false',
    );
    if (useLocalDev == 'true') {
      return kIsWeb ? webDevApiBaseUrl : devApiBaseUrl;
    }

    return vercelApiBaseUrl;
  }
}
