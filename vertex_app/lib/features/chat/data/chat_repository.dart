import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../domain/models/prediction_models.dart';
import 'chat_api.dart';

class ChatRepository {
  ChatRepository(this._api);

  final ChatApi _api;

  Future<PredictionResponse> classify(String text, {bool forceClassify = false}) {
    return _api.predict(text, forceClassify: forceClassify);
  }
}

final chatRepositoryProvider = Provider<ChatRepository>((ref) {
  return ChatRepository(ref.read(chatApiProvider));
});
