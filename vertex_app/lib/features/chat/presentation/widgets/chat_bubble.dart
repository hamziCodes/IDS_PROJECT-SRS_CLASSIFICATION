import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/utils/date_utils.dart';
import '../../../../core/widgets/glass_container.dart';
import '../../domain/models/chat_message.dart';
import '../../domain/models/prediction_models.dart';

class ChatBubble extends StatelessWidget {
  const ChatBubble({
    super.key,
    required this.message,
    required this.onDownloadPrediction,
  });

  final ChatMessage message;
  final void Function(PredictionResponse prediction) onDownloadPrediction;

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
            crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
            children: [
              if (message.prediction != null && !isUser)
                GlassContainer(
                  child: _PredictionContent(
                    prediction: message.prediction!,
                    onDownload: () => onDownloadPrediction(message.prediction!),
                  ),
                )
              else
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: isUser ? bubbleColor : AppColors.surfaceSoft,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text(message.text, style: Theme.of(context).textTheme.bodyMedium),
                ),
              const SizedBox(height: 6),
              Text(
                DateUtilsX.formatDateTime(message.timestamp),
                style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _PredictionContent extends StatelessWidget {
  const _PredictionContent({required this.prediction, required this.onDownload});

  final PredictionResponse prediction;
  final VoidCallback onDownload;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Expanded(
              child: Text('Classification Results', style: Theme.of(context).textTheme.titleLarge),
            ),
            TextButton.icon(
              onPressed: onDownload,
              icon: const Icon(Icons.download_rounded, size: 18),
              label: const Text('Download Results'),
            ),
          ],
        ),
        const SizedBox(height: 8),
        _categorySection(context, 'Functional Requirements', prediction.functionalRequirements, AppColors.success),
        const SizedBox(height: 10),
        _categorySection(context, 'Non-Functional Requirements', prediction.nonFunctionalRequirements, AppColors.warning),
        const SizedBox(height: 10),
        _categorySection(context, 'Neither', prediction.neither, AppColors.textSecondary),
      ],
    );
  }

  Widget _categorySection(
    BuildContext context,
    String title,
    List<RequirementItem> items,
    Color accent,
  ) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: ExpansionTile(
        key: PageStorageKey<String>('classification-$title'),
        initiallyExpanded: false,
        tilePadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        childrenPadding: const EdgeInsets.fromLTRB(14, 0, 14, 14),
        collapsedBackgroundColor: AppColors.surfaceSoft.withValues(alpha: 0.65),
        backgroundColor: AppColors.surfaceSoft,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        collapsedShape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        iconColor: accent,
        collapsedIconColor: accent,
        textColor: Theme.of(context).textTheme.bodyLarge?.color,
        collapsedTextColor: Theme.of(context).textTheme.bodyLarge?.color,
        title: Row(
          children: [
            Container(width: 8, height: 8, decoration: BoxDecoration(color: accent, shape: BoxShape.circle)),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                title,
                style: Theme.of(context).textTheme.bodyLarge,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const SizedBox(width: 8),
            Text(
              '${items.length}',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
            ),
          ],
        ),
        children: [
          if (items.isEmpty)
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'No items',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
              ),
            )
          else
            Column(
              children: items
                  .map(
                    (item) => Container(
                      margin: const EdgeInsets.only(bottom: 6),
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: AppColors.surface,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(item.text, style: Theme.of(context).textTheme.bodyMedium),
                          if (item.confidence != null) ...[
                            const SizedBox(height: 4),
                            Text(
                              'Confidence: ${(item.confidence! * 100).toStringAsFixed(1)}%',
                              style: Theme.of(context)
                                  .textTheme
                                  .bodySmall
                                  ?.copyWith(color: AppColors.textSecondary),
                            ),
                          ],
                          if (item.nfrTypes.isNotEmpty) ...[
                            const SizedBox(height: 6),
                            Wrap(
                              spacing: 6,
                              runSpacing: 6,
                              children: item.nfrTypes
                                  .map(
                                    (type) => Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: AppColors.surfaceSoft,
                                        borderRadius: BorderRadius.circular(10),
                                      ),
                                      child: Text(type, style: Theme.of(context).textTheme.bodySmall),
                                    ),
                                  )
                                  .toList(),
                            ),
                          ],
                          if (item.isOutlier) ...[
                            const SizedBox(height: 6),
                            Text(
                              item.outlierProbability == null
                                  ? 'Flagged as outlier'
                                  : 'Outlier probability: ${(item.outlierProbability! * 100).toStringAsFixed(1)}%',
                              style: Theme.of(context)
                                  .textTheme
                                  .bodySmall
                                  ?.copyWith(color: AppColors.textSecondary),
                            ),
                          ],
                        ],
                      ),
                    ),
                  )
                  .toList(),
            ),
        ],
      ),
    );
  }
}
