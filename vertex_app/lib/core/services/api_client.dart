import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';

class ApiClient {
  ApiClient()
      : _dio = Dio(
          BaseOptions(
            baseUrl: AppConfig.apiBaseUrl,
            connectTimeout: const Duration(seconds: 10),
            receiveTimeout: const Duration(seconds: 30),
            headers: {'Content-Type': 'application/json'},
          ),
        );

  final Dio _dio;

  Future<Response<dynamic>> get(String path) => _dio.get(path);

  Future<Response<dynamic>> post(String path, {Map<String, dynamic>? data}) {
    return _dio.post(path, data: data);
  }
}

final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());
