import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

import '../../../../core/services/storage_service.dart';
import '../../data/chat_repository.dart';
import '../../domain/models/chat_message.dart';
import '../../domain/models/prediction_models.dart';

class ChatState {
  ChatState({
    required this.messages,
    required this.isLoading,
    this.errorMessage,
    this.lastPrediction,
    this.lastUserInput,
  });

  final List<ChatMessage> messages;
  final bool isLoading;
  final String? errorMessage;
  final PredictionResponse? lastPrediction;
  final String? lastUserInput;

  ChatState copyWith({
    List<ChatMessage>? messages,
    bool? isLoading,
    String? errorMessage,
    PredictionResponse? lastPrediction,
    String? lastUserInput,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: errorMessage,
      lastPrediction: lastPrediction ?? this.lastPrediction,
      lastUserInput: lastUserInput ?? this.lastUserInput,
    );
  }

  factory ChatState.initial() => ChatState(messages: const [], isLoading: false);
}

class ChatController extends StateNotifier<ChatState> {
  ChatController(this._repository) : super(ChatState.initial());

  final ChatRepository _repository;
  final _uuid = const Uuid();

  Future<void> sendMessage(String text) async {
    final trimmed = text.trim();
    if (trimmed.isEmpty) {
      return;
    }

    final userMessage = ChatMessage(
      id: _uuid.v4(),
      role: MessageRole.user,
      text: trimmed,
      timestamp: DateTime.now(),
    );

    state = state.copyWith(
      messages: [...state.messages, userMessage],
      isLoading: true,
      errorMessage: null,
      lastUserInput: trimmed,
    );

    try {
      final response = await _repository.classify(trimmed);
      final assistantMessage = ChatMessage(
        id: _uuid.v4(),
        role: MessageRole.assistant,
        text: _buildSummary(response),
        timestamp: DateTime.now(),
        prediction: response,
      );

      state = state.copyWith(
        messages: [...state.messages, assistantMessage],
        isLoading: false,
        lastPrediction: response,
      );

      await StorageService.saveLastResponse(jsonEncode(response.toJson()));
    } catch (error) {
      final cached = await StorageService.loadLastResponse();
      ChatMessage fallbackMessage;

      if (cached != null) {
        final cachedResponse = PredictionResponse.fromJson(
          jsonDecode(cached) as Map<String, dynamic>,
        );
        fallbackMessage = ChatMessage(
          id: _uuid.v4(),
          role: MessageRole.assistant,
          text: 'Showing the last saved response because the service is unreachable.',
          timestamp: DateTime.now(),
          prediction: cachedResponse,
        );
      } else {
        fallbackMessage = ChatMessage(
          id: _uuid.v4(),
          role: MessageRole.system,
          text: 'Unable to reach the classification service. Please try again.',
          timestamp: DateTime.now(),
        );
      }

      state = state.copyWith(
        messages: [...state.messages, fallbackMessage],
        isLoading: false,
        errorMessage: 'Service unavailable',
      );
    }
  }

  Future<void> retryLast() async {
    final lastInput = state.lastUserInput;
    if (lastInput != null) {
      await sendMessage(lastInput);
    }
  }

  String _buildSummary(PredictionResponse response) {
    return 'Classification complete: '
        '${response.counts['functional'] ?? 0} functional, '
        '${response.counts['non_functional'] ?? 0} non-functional, '
        '${response.counts['neither'] ?? 0} neither.';
  }
}

final chatControllerProvider = StateNotifierProvider<ChatController, ChatState>((ref) {
  return ChatController(ref.read(chatRepositoryProvider));
});
