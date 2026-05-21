import 'package:flutter/material.dart';

import '../constants/app_constants.dart';
import '../theme/app_colors.dart';

class VertexAppBar extends StatelessWidget implements PreferredSizeWidget {
  const VertexAppBar({
    super.key,
    this.onShare,
    this.showShare = false,
    this.showBack = false,
  });

  final VoidCallback? onShare;
  final bool showShare;
  final bool showBack;

  @override
  Size get preferredSize => const Size.fromHeight(70);

  @override
  Widget build(BuildContext context) {
    return AppBar(
      automaticallyImplyLeading: true,
      titleSpacing: 16,
      title: Row(
        children: [
          Hero(
            tag: 'vertexLogo',
            child: Image.asset(
              'assets/images/logo_nobg.png',
              width: 28,
              height: 28,
            ),
          ),
          const SizedBox(width: 10),
          Text(
            AppConstants.appName,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(color: AppColors.textPrimary),
          ),
        ],
      ),
      actions: [
        if (showShare)
          IconButton(
            icon: const Icon(Icons.share_outlined),
            onPressed: onShare,
          ),
      ],
    );
  }
}
