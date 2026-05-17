import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../../core/services/export_service.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/utils/date_utils.dart';
import '../../../../core/utils/web_download_util.dart';
import '../../../../core/widgets/glass_container.dart';
import '../../domain/models/chat_message.dart';
import '../../domain/models/prediction_models.dart';
import 'collapsible_category_section.dart';

class ChatBubble extends StatelessWidget {
  const ChatBubble({super.key, required this.message});

  final ChatMessage message;

  @override
  Widget build(BuildContext context) {
    final isUser = message.role == MessageRole.user;
    final alignment = isUser ? Alignment.centerRight : Alignment.centerLeft;
    final bubbleColor = isUser ? AppColors.accent : AppColors.surfaceSoft;

    return TweenAnimationBuilder<double>(
      duration: const Duration(milliseconds: 320),
      tween: Tween(begin: 0, end: 1),
      builder: (context, value, child) {
        return Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, (1 - value) * 12),
            child: child,
          ),
        );
      },
      child: Align(
        alignment: alignment,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 8),
          child: Column(
            crossAxisAlignment: isUser
                ? CrossAxisAlignment.end
                : CrossAxisAlignment.start,
            children: [
              if (message.prediction != null && !isUser)
                GlassContainer(
                  child: _PredictionContent(prediction: message.prediction!),
                )
              else
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                  decoration: BoxDecoration(
                    color: isUser ? bubbleColor : AppColors.surfaceSoft,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(
                    message.text,
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ),
              const SizedBox(height: 6),
              Text(
                DateUtilsX.formatDateTime(message.timestamp),
                style: Theme.of(
                  context,
                ).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PredictionContent extends StatelessWidget {
  const _PredictionContent({required this.prediction});

  final PredictionResponse prediction;

  void _downloadResults(BuildContext context) {
    try {
      final csvContent = ExportService.generateCsv(prediction);
      final filename = ExportService.generateFilename();

      if (kIsWeb) {
        _downloadWebCsv(csvContent, filename);
      } else {
        _showMessage(context, 'Download will be supported soon on mobile!');
        return;
      }

      _showMessage(context, 'Downloaded $filename', isSuccess: true);
    } catch (e) {
      _showMessage(context, 'Error: ${e.toString()}', isSuccess: false);
    }
  }

  void _downloadWebCsv(String csvContent, String filename) {
    WebDownloadUtil.downloadCsv(csvContent, filename);
  }

  void _showMessage(
    BuildContext context,
    String message, {
    bool isSuccess = true,
  }) {
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: const Duration(seconds: 2),
        backgroundColor: isSuccess ? AppColors.success : AppColors.warning,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Classification Results',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            GestureDetector(
              onTap: () => _downloadResults(context),
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  color: AppColors.accent.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: AppColors.accent.withOpacity(0.3),
                    width: 1,
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.download_rounded,
                      color: AppColors.accent,
                      size: 16,
                    ),
                    const SizedBox(width: 6),
                    Text(
                      'Download',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: AppColors.accent,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        CollapsibleCategorySection(
          title: 'Functional Requirements (FR)',
          items: prediction.functionalRequirements,
          accentColor: AppColors.success,
        ),
        const SizedBox(height: 12),
        CollapsibleCategorySection(
          title: 'Non-Functional Requirements (NFR)',
          items: prediction.nonFunctionalRequirements,
          accentColor: AppColors.warning,
        ),
        const SizedBox(height: 12),
        CollapsibleCategorySection(
          title: 'Neither',
          items: prediction.neither,
          accentColor: AppColors.textSecondary,
        ),
      ],
    );
  }
}
