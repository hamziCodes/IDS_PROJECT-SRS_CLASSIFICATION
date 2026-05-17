import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_client.dart';
import '../domain/model_info.dart';

class ModelRepository {
  ModelRepository(this._client);

  final ApiClient _client;

  Future<ModelInfo> fetchModelInfo() async {
    final response = await _client.get('/model-info');
    return ModelInfo.fromJson(response.data as Map<String, dynamic>);
  }
}

final modelRepositoryProvider = Provider<ModelRepository>((ref) {
  return ModelRepository(ref.read(apiClientProvider));
});
