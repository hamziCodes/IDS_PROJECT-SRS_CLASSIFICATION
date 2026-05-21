import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

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
  Future<void> _openExpandedComposer() async {
    final result = await showGeneralDialog<String>(
      context: context,
      barrierDismissible: true,
      barrierLabel: 'Expanded Composer',
      barrierColor: Colors.black.withValues(alpha: 0.72),
      transitionDuration: const Duration(milliseconds: 280),
      pageBuilder: (context, _, _) {
        return _ExpandedComposerDialog(initialText: widget.controller.text);
      },
      transitionBuilder: (context, animation, secondaryAnimation, child) {
        final curved = CurvedAnimation(parent: animation, curve: Curves.easeOutCubic);
        return FadeTransition(
          opacity: curved,
          child: SlideTransition(
            position: Tween<Offset>(begin: const Offset(0, 0.03), end: Offset.zero).animate(curved),
            child: child,
          ),
        );
      },
    );

    if (result == null || !mounted) {
      return;
    }
    widget.controller.value = TextEditingValue(
      text: result,
      selection: TextSelection.collapsed(offset: result.length),
    );
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final canSend = widget.controller.text.trim().isNotEmpty && !widget.isLoading;

    return Container(
      constraints: const BoxConstraints(minHeight: 56),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: const Color(0xFF1F1F1F),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.white.withOpacity(0.06)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Expanded(
            child: AnimatedSize(
              duration: const Duration(milliseconds: 220),
              curve: Curves.easeOutCubic,
              child: TextField(
                controller: widget.controller,
                minLines: 1,
                maxLines: 3,
                keyboardType: TextInputType.multiline,
                textInputAction: TextInputAction.newline,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: AppColors.textPrimary),
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
                ),
                onChanged: (_) => setState(() {}),
              ),
            ),
          ),
          IconButton(
            onPressed: _openExpandedComposer,
            icon: const Icon(Icons.open_in_full_rounded, color: AppColors.textSecondary),
            tooltip: 'Expand input',
          ),
          IconButton(
            onPressed: canSend ? widget.onSend : null,
            icon: Icon(
              Icons.send_rounded,
              color: canSend ? AppColors.accentSoft : AppColors.textSecondary.withValues(alpha: 0.5),
            ),
            tooltip: 'Send',
          ),
        ],
      ),
    );
  }
}

class _ExpandedComposerDialog extends StatefulWidget {
  const _ExpandedComposerDialog({required this.initialText});

  final String initialText;

  @override
  State<_ExpandedComposerDialog> createState() => _ExpandedComposerDialogState();
}

class _ExpandedComposerDialogState extends State<_ExpandedComposerDialog> {
  late final TextEditingController _draftController;

  @override
  void initState() {
    super.initState();
    _draftController = TextEditingController(text: widget.initialText);
  }

  @override
  void dispose() {
    _draftController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Material(
        color: AppColors.background,
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(12, 10, 12, 8),
              child: Row(
                children: [
                  IconButton(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.close_rounded, color: AppColors.textPrimary),
                    tooltip: 'Close',
                  ),
                  Expanded(
                    child: Text(
                      'Expanded Input',
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                  ),
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(_draftController.text),
                    child: const Text('Done'),
                  ),
                ],
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
                child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceSoft,
                    borderRadius: BorderRadius.circular(18),
                    border: Border.all(color: Colors.white.withValues(alpha: 0.08)),
                  ),
                  child: TextField(
                    controller: _draftController,
                    autofocus: true,
                    expands: true,
                    maxLines: null,
                    minLines: null,
                    keyboardType: TextInputType.multiline,
                    style: Theme.of(context).textTheme.bodyLarge,
                    cursorColor: AppColors.textPrimary,
                    decoration: const InputDecoration(
                      hintText: 'Paste or type large requirement blocks here...',
                      hintStyle: TextStyle(color: AppColors.textSecondary),
                      border: InputBorder.none,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
