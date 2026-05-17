import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import 'expanded_input_modal.dart';

class ChatInputBar extends StatefulWidget {
  const ChatInputBar({
    super.key,
    required this.controller,
    required this.onSend,
    this.isLoading = false,
  });

  final TextEditingController controller;
  final VoidCallback onSend;
  final bool isLoading;

  @override
  State<ChatInputBar> createState() => _ChatInputBarState();
}

class _ChatInputBarState extends State<ChatInputBar> {
  late TextEditingController _internalController;
  double _inputHeight = 52;
  static const double _minHeight = 52; // 1 line
  static const double _maxHeight = 98; // 3 lines (~18 pixels each + padding)
  static const double _lineHeight = 20;

  @override
  void initState() {
    super.initState();
    _internalController = widget.controller;
    _internalController.addListener(_updateHeight);
  }

  @override
  void dispose() {
    _internalController.removeListener(_updateHeight);
    super.dispose();
  }

  void _updateHeight() {
    final text = _internalController.text;
    if (text.isEmpty) {
      _setHeight(_minHeight);
      return;
    }

    // Count newlines to estimate line count
    final lineCount = '\n'.allMatches(text).length + 1;
    final estimatedHeight = _minHeight + ((lineCount - 1) * _lineHeight) + 8;

    if (estimatedHeight >= _maxHeight) {
      _setHeight(_maxHeight);
    } else {
      _setHeight(estimatedHeight);
    }
  }

  void _setHeight(double height) {
    if (_inputHeight != height) {
      setState(() {
        _inputHeight = height;
      });
    }
  }

  void _openExpandedInput() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => ExpandedInputModal(
          controller: _internalController,
          onClose: () => Navigator.of(context).pop(),
        ),
        fullscreenDialog: true,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      curve: Curves.easeOut,
      height: _inputHeight,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF1F1F1F),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.06)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Expanded(
            child: TextField(
              controller: _internalController,
              maxLines: null,
              minLines: 1,
              style: Theme.of(
                context,
              ).textTheme.bodyLarge?.copyWith(color: AppColors.textPrimary),
              cursorColor: AppColors.textPrimary,
              decoration: const InputDecoration(
                hintText: 'Ask anything',
                hintStyle: TextStyle(color: AppColors.textSecondary),
                border: InputBorder.none,
                enabledBorder: InputBorder.none,
                focusedBorder: InputBorder.none,
                filled: true,
                fillColor: Colors.transparent,
                isDense: true,
                contentPadding: EdgeInsets.symmetric(
                  horizontal: 4,
                  vertical: 0,
                ),
              ),
              textInputAction: TextInputAction.newline,
              onSubmitted: (_) {
                // Allow newline on Shift+Enter, manual send only on button
              },
            ),
          ),
          const SizedBox(width: 8),
          // Expand button
          GestureDetector(
            onTap: _openExpandedInput,
            child: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.white.withOpacity(0.1)),
              ),
              child: Icon(
                Icons.unfold_more_rounded,
                color: AppColors.textSecondary,
                size: 18,
              ),
            ),
          ),
          const SizedBox(width: 8),
          GestureDetector(
            onTap: widget.isLoading ? null : widget.onSend,
            child: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: widget.isLoading
                    ? AppColors.accent.withOpacity(0.5)
                    : AppColors.accent,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(
                widget.isLoading ? Icons.hourglass_empty : Icons.send_rounded,
                color: Colors.white,
                size: 18,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
