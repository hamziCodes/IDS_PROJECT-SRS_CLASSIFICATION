import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/widgets/glass_container.dart';

class ConfusionMatrixCard extends StatelessWidget {
  const ConfusionMatrixCard({super.key, required this.matrix, required this.labels});

  final List<List<int>> matrix;
  final List<String> labels;

  @override
  Widget build(BuildContext context) {
    if (matrix.length < 2) {
      return const SizedBox.shrink();
    }

    return GlassContainer(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Confusion Matrix', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          Table(
            border: TableBorder.all(color: Colors.white12),
            children: [
              TableRow(
                children: [
                  const SizedBox(),
                  _headerCell(labels[0]),
                  _headerCell(labels[1]),
                ],
              ),
              TableRow(
                children: [
                  _headerCell(labels[0]),
                  _valueCell(matrix[0][0]),
                  _valueCell(matrix[0][1]),
                ],
              ),
              TableRow(
                children: [
                  _headerCell(labels[1]),
                  _valueCell(matrix[1][0]),
                  _valueCell(matrix[1][1]),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _headerCell(String label) {
    return Container(
      padding: const EdgeInsets.all(8),
      color: AppColors.surfaceSoft,
      child: Text(label, textAlign: TextAlign.center),
    );
  }

  Widget _valueCell(int value) {
    return Container(
      padding: const EdgeInsets.all(12),
      child: Text(value.toString(), textAlign: TextAlign.center),
    );
  }
}
