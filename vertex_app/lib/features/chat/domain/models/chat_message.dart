import 'prediction_models.dart';

enum MessageRole { user, assistant, system }

class ChatMessage {
  ChatMessage({
    required this.id,
    required this.role,
    required this.text,
    required this.timestamp,
    this.prediction,
  });

  final String id;
  final MessageRole role;
  final String text;
  final DateTime timestamp;
  final PredictionResponse? prediction;
}
