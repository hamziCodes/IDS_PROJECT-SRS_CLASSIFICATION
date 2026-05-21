import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../constants/app_constants.dart';
import '../theme/app_colors.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: AppColors.surface,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [AppColors.backgroundAlt, AppColors.surface],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Row(
              children: [
                Image.asset('assets/images/logo_nobg.png', width: 36, height: 36),
                const SizedBox(width: 12),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(AppConstants.appName, style: Theme.of(context).textTheme.titleLarge),
                    const SizedBox(height: 4),
                    Text(AppConstants.appTagline, style: Theme.of(context).textTheme.bodyMedium),
                  ],
                ),
              ],
            ),
          ),
          _drawerItem(context, Icons.chat_bubble_outline, 'Home', '/home'),
          _drawerItem(context, Icons.memory, 'Model', '/model'),
          _drawerItem(context, Icons.info_outline, 'About Us', '/about'),
          const Spacer(),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              'Vertex - AI Studio',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(color: AppColors.textSecondary),
            ),
          ),
        ],
      ),
    );
  }

  Widget _drawerItem(BuildContext context, IconData icon, String label, String route) {
    return ListTile(
      leading: Icon(icon, color: AppColors.textPrimary),
      title: Text(label, style: Theme.of(context).textTheme.bodyLarge),
      onTap: () {
        Navigator.of(context).pop();
        context.go(route);
      },
    );
  }
}
