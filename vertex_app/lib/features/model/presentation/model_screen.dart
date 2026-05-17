import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shimmer/shimmer.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/widgets/app_drawer.dart';
import '../../../core/widgets/gradient_scaffold.dart';
import '../../../core/widgets/section_header.dart';
import '../../../core/widgets/vertex_app_bar.dart';
import '../data/model_repository.dart';
import '../domain/model_info.dart';
import 'widgets/confusion_matrix_card.dart';
import 'widgets/metric_card.dart';

final modelInfoProvider = FutureProvider<ModelInfo>((ref) {
  return ref.read(modelRepositoryProvider).fetchModelInfo();
});

class ModelScreen extends ConsumerWidget {
  const ModelScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final modelInfoAsync = ref.watch(modelInfoProvider);

    return GradientScaffold(
      appBar: const VertexAppBar(showShare: false),
      drawer: const AppDrawer(),
      body: modelInfoAsync.when(
        data: (info) => _ModelContent(info: info),
        loading: () => const _ModelSkeleton(),
        error: (error, stack) => Center(
          child: Text(
            'Unable to load model info',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
        ),
      ),
    );
  }
}

class _ModelSkeleton extends StatelessWidget {
  const _ModelSkeleton();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Column(
        children: [
          _shimmerBlock(height: 24, width: double.infinity),
          const SizedBox(height: 12),
          _shimmerBlock(height: 120, width: double.infinity),
          const SizedBox(height: 12),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: [
              _shimmerBlock(height: 90, width: 160),
              _shimmerBlock(height: 90, width: 160),
              _shimmerBlock(height: 90, width: 160),
              _shimmerBlock(height: 90, width: 160),
            ],
          ),
          const SizedBox(height: 12),
          _shimmerBlock(height: 180, width: double.infinity),
        ],
      ),
    );
  }

  Widget _shimmerBlock({required double height, required double width}) {
    return Shimmer.fromColors(
      baseColor: Colors.white12,
      highlightColor: Colors.white24,
      child: Container(
        height: height,
        width: width,
        decoration: BoxDecoration(
          color: Colors.white12,
          borderRadius: BorderRadius.circular(16),
        ),
      ),
    );
  }
}

class _ModelContent extends StatelessWidget {
  const _ModelContent({required this.info});

  final ModelInfo info;

  @override
  Widget build(BuildContext context) {
    final metrics = info.metrics;
    final matrix = (metrics['confusion_matrix'] as List<dynamic>? ?? [])
        .map(
          (row) =>
              (row as List<dynamic>).map((v) => (v as num).toInt()).toList(),
        )
        .toList();
    final labels =
        (metrics['labels'] as List<dynamic>? ??
                ['Non-Functional', 'Functional'])
            .map((e) => e.toString())
            .toList();

    final hasFullMetrics =
        metrics['precision'] != null && metrics['recall'] != null;
    final accuracy = _number(metrics['accuracy']) ??
        _number(info.metadata['accuracy_fr_nfr']) ??
        0;
    final precision = _number(metrics['precision']) ?? 0;
    final recall = _number(metrics['recall']) ?? 0;
    final f1 = _number(metrics['f1']) ??
        _number(metrics['nfr_type_weighted_f1']) ??
        _number(info.metadata['weighted_f1_nfr_types']) ??
        0;
    final nfrAccuracy = _number(metrics['nfr_type_accuracy']) ??
        _number(info.metadata['accuracy_nfr_types']) ??
        0;
    final hammingLoss = _number(metrics['nfr_type_hamming_loss']) ??
        _number(info.metadata['hamming_loss_nfr_types']) ??
        0;

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SectionHeader(title: 'Model Overview', subtitle: info.modelName),
          const SizedBox(height: 6),
          Text(
            'Vertex classifies software requirements into functional, non-functional, and neither. '
            'It uses TF-IDF features and logistic regression for FR/NFR, plus a multi-output classifier for NFR types.',
            style: Theme.of(
              context,
            ).textTheme.bodyMedium?.copyWith(color: AppColors.textSecondary),
          ),
          const SizedBox(height: 18),
          SectionHeader(
            title: 'Performance Metrics',
            subtitle: 'Live metrics from the training dataset.',
          ),
          const SizedBox(height: 12),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            children: hasFullMetrics
                ? [
                    MetricCard(
                      label: 'Accuracy',
                      value: accuracy * 100,
                      suffix: '%',
                    ),
                    MetricCard(
                      label: 'Precision',
                      value: precision * 100,
                      suffix: '%',
                    ),
                    MetricCard(
                      label: 'Recall',
                      value: recall * 100,
                      suffix: '%',
                    ),
                    MetricCard(label: 'F1-Score', value: f1 * 100, suffix: '%'),
                  ]
                : [
                    MetricCard(
                      label: 'FR/NFR Accuracy',
                      value: accuracy * 100,
                      suffix: '%',
                    ),
                    MetricCard(
                      label: 'NFR Accuracy',
                      value: nfrAccuracy * 100,
                      suffix: '%',
                    ),
                    MetricCard(
                      label: 'NFR F1',
                      value: f1 * 100,
                      suffix: '%',
                    ),
                    MetricCard(
                      label: 'Hamming Loss',
                      value: hammingLoss * 100,
                      suffix: '%',
                    ),
                  ],
          ),
          const SizedBox(height: 16),
          ConfusionMatrixCard(matrix: matrix, labels: labels),
          const SizedBox(height: 18),
          SectionHeader(title: 'Dataset + Features'),
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.surfaceSoft,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white.withOpacity(0.06)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Key stats',
                  style: Theme.of(context).textTheme.titleSmall,
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  children: [
                    _statCard(
                      context,
                      'Vocabulary Size',
                      info.metadata['vocab_size'],
                    ),
                    _statCard(
                      context,
                      'Training Samples',
                      info.metadata['n_train'],
                    ),
                    _statCard(context, 'Test Samples', info.metadata['n_test']),
                  ],
                ),
                const SizedBox(height: 16),
                Divider(color: Colors.white.withOpacity(0.08)),
                const SizedBox(height: 12),
                Text(
                  'NFR Types',
                  style: Theme.of(context).textTheme.titleSmall,
                ),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: info.nfrTypes
                      .map((type) => _nfrChip(context, type))
                      .toList(),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),
          SectionHeader(title: 'Classification Pipeline'),
          _bullet(context, 'Outlier gate using rules + logistic classifier'),
          _bullet(context, 'TF-IDF vectorization with unigrams and bigrams'),
          _bullet(context, 'Binary FR/NFR classifier'),
          _bullet(context, 'Multi-label NFR type classifier'),
          const SizedBox(height: 18),
          SectionHeader(title: 'Technologies Used'),
          _bullet(context, 'Python, Scikit-learn, NLTK, Pandas'),
          _bullet(context, 'FastAPI backend'),
          _bullet(context, 'Flutter + Riverpod mobile client'),
        ],
      ),
    );
  }

  double? _number(Object? value) {
    return value is num ? value.toDouble() : null;
  }

  Widget _infoRow(BuildContext context, String label, Object? value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Expanded(
            child: Text(
              label,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ),
          Expanded(
            child: Text(
              value?.toString() ?? '--',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.end,
              style: Theme.of(
                context,
              ).textTheme.bodyMedium?.copyWith(color: AppColors.textSecondary),
            ),
          ),
        ],
      ),
    );
  }

  Widget _statCard(BuildContext context, String label, Object? value) {
    return Container(
      width: 180,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white.withOpacity(0.06)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: Theme.of(
              context,
            ).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
          ),
          const SizedBox(height: 6),
          Text(
            value?.toString() ?? '--',
            style: Theme.of(context).textTheme.titleMedium,
          ),
        ],
      ),
    );
  }

  Widget _nfrChip(BuildContext context, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: AppColors.backgroundAlt,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: Colors.white.withOpacity(0.08)),
      ),
      child: Text(
        label,
        style: Theme.of(
          context,
        ).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
      ),
    );
  }

  Widget _bullet(BuildContext context, String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(top: 6),
            child: Icon(Icons.circle, size: 6, color: AppColors.accentSoft),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Text(text, style: Theme.of(context).textTheme.bodyMedium),
          ),
        ],
      ),
    );
  }
}
