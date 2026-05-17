import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  static const String _lastResponseKey = 'last_prediction_response';

  static Future<void> saveLastResponse(String json) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_lastResponseKey, json);
  }

  static Future<String?> loadLastResponse() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_lastResponseKey);
  }
}
