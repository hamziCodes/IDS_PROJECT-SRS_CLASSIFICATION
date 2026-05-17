import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_client.dart';
import '../domain/models/prediction_models.dart';

class ChatApi {
  ChatApi(this._client);

  final ApiClient _client;

  Future<PredictionResponse> predict(String text, {bool forceClassify = false}) async {
    final response = await _client.post(
      '/predict',
      data: {
        'text': text,
        'force_classify': forceClassify,
      },
    );
    return PredictionResponse.fromJson(response.data as Map<String, dynamic>);
  }
}

final chatApiProvider = Provider<ChatApi>((ref) => ChatApi(ref.read(apiClientProvider)));
