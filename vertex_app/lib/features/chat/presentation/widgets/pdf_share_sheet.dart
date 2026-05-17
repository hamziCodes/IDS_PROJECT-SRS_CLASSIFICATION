import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

class PdfShareSheet extends StatelessWidget {
  const PdfShareSheet({super.key, required this.onShare, required this.onDownload});

  final VoidCallback onShare;
  final VoidCallback onDownload;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: const BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Export PDF', style: Theme.of(context).textTheme.titleLarge),
          const SizedBox(height: 12),
          ListTile(
            leading: const Icon(Icons.share_outlined, color: AppColors.textPrimary),
            title: const Text('Share as PDF'),
            subtitle: const Text('Send to apps or collaborators'),
            onTap: onShare,
          ),
          ListTile(
            leading: const Icon(Icons.download_outlined, color: AppColors.textPrimary),
            title: const Text('Download PDF'),
            subtitle: const Text('Save locally on this device'),
            onTap: onDownload,
          ),
        ],
      ),
    );
  }
}
