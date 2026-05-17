import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../domain/models/prediction_models.dart';

class CollapsibleCategorySection extends StatefulWidget {
  const CollapsibleCategorySection({
    super.key,
    required this.title,
    required this.items,
    required this.accentColor,
  });

  final String title;
  final List<RequirementItem> items;
  final Color accentColor;

  @override
  State<CollapsibleCategorySection> createState() =>
      _CollapsibleCategorySectionState();
}

class _CollapsibleCategorySectionState extends State<CollapsibleCategorySection>
    with SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _heightAnimation;
  bool _isExpanded = false;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _heightAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  void _toggleExpand() {
    setState(() {
      _isExpanded = !_isExpanded;
    });
    if (_isExpanded) {
      _animationController.forward();
    } else {
      _animationController.reverse();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Header/Clickable Section
        GestureDetector(
          onTap: _toggleExpand,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
            decoration: BoxDecoration(
              color: AppColors.surface.withOpacity(0.5),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: widget.accentColor.withOpacity(0.3),
                width: 1,
              ),
            ),
            child: Row(
              children: [
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    color: widget.accentColor,
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    widget.title,
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                // Count badge
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: widget.accentColor.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    '${widget.items.length}',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: widget.accentColor,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                // Chevron icon with rotation animation
                RotationTransition(
                  turns: Tween<double>(
                    begin: 0,
                    end: 0.5,
                  ).animate(_animationController),
                  child: Icon(
                    Icons.expand_more,
                    color: widget.accentColor,
                    size: 20,
                  ),
                ),
              ],
            ),
          ),
        ),
        // Expandable content
        SizeTransition(
          sizeFactor: _heightAnimation,
          axisAlignment: -1.0,
          child: Padding(
            padding: const EdgeInsets.only(top: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (widget.items.isEmpty)
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    child: Text(
                      'No items in this category',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.textSecondary,
                      ),
                    ),
                  )
                else
                  Column(
                    children: widget.items
                        .asMap()
                        .entries
                        .map(
                          (entry) => _buildRequirementItem(
                            context,
                            entry.value,
                            entry.key,
                          ),
                        )
                        .toList(),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildRequirementItem(
    BuildContext context,
    RequirementItem item,
    int index,
  ) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.surfaceSoft, width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Requirement text with index
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 24,
                height: 24,
                decoration: BoxDecoration(
                  color: widget.accentColor.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Center(
                  child: Text(
                    '${index + 1}',
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: widget.accentColor,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  item.text,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
            ],
          ),
          // Confidence
          if (item.confidence != null) ...[
            const SizedBox(height: 8),
            Row(
              children: [
                const SizedBox(width: 34),
                Text(
                  'Confidence: ',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
                Expanded(
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(4),
                    child: LinearProgressIndicator(
                      value: item.confidence,
                      minHeight: 6,
                      backgroundColor: AppColors.surface,
                      valueColor: AlwaysStoppedAnimation<Color>(
                        widget.accentColor.withOpacity(0.6),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  '${(item.confidence! * 100).toStringAsFixed(0)}%',
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: widget.accentColor,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ],
          // NFR Types
          if (item.nfrTypes.isNotEmpty) ...[
            const SizedBox(height: 8),
            const SizedBox(width: 34),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: item.nfrTypes
                  .map(
                    (type) => Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: widget.accentColor.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: widget.accentColor.withOpacity(0.3),
                          width: 0.5,
                        ),
                      ),
                      child: Text(
                        type,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                          color: widget.accentColor,
                        ),
                      ),
                    ),
                  )
                  .toList(),
            ),
          ],
          // Outlier info
          if (item.isOutlier) ...[
            const SizedBox(height: 8),
            const SizedBox(width: 34),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
              decoration: BoxDecoration(
                color: AppColors.warning.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: AppColors.warning.withOpacity(0.3),
                  width: 0.5,
                ),
              ),
              child: Text(
                item.outlierProbability == null
                    ? 'Flagged as outlier'
                    : 'Outlier probability: ${(item.outlierProbability! * 100).toStringAsFixed(1)}%',
                style: Theme.of(
                  context,
                ).textTheme.bodySmall?.copyWith(color: AppColors.warning),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
