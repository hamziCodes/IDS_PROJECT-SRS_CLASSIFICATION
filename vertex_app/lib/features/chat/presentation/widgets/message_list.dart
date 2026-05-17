import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../controller/chat_controller.dart';
import 'chat_bubble.dart';
import 'typing_indicator.dart';

class MessageList extends ConsumerWidget {
  const MessageList({super.key, required this.scrollController});

  final ScrollController scrollController;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(chatControllerProvider);
    final messages = state.messages;

    if (messages.isEmpty && !state.isLoading) {
      return Center(
        child: Text(
          'No messages yet. Start by pasting a requirement.',
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.white70),
          textAlign: TextAlign.center,
        ),
      );
    }

    return ListView.builder(
      controller: scrollController,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      itemCount: messages.length + (state.isLoading ? 1 : 0),
      itemBuilder: (context, index) {
        if (state.isLoading && index == messages.length) {
          return const Padding(
            padding: EdgeInsets.symmetric(vertical: 8),
            child: TypingIndicator(),
          );
        }

        return ChatBubble(message: messages[index]);
      },
    );
  }
}
