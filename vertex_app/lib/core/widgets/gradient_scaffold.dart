import 'package:flutter/material.dart';

import '../theme/app_colors.dart';

class GradientScaffold extends StatelessWidget {
  const GradientScaffold({
    super.key,
    required this.body,
    this.appBar,
    this.drawer,
    this.floatingActionButton,
  });

  final Widget body;
  final PreferredSizeWidget? appBar;
  final Widget? drawer;
  final Widget? floatingActionButton;

  @override
  Widget build(BuildContext context) {
    final safeBody = SafeArea(
      top: appBar == null,
      bottom: true,
      child: body,
    );

    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.background, AppColors.backgroundAlt],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Scaffold(
        backgroundColor: Colors.transparent,
        extendBody: true,
        resizeToAvoidBottomInset: true,
        appBar: appBar,
        drawer: drawer,
        floatingActionButton: floatingActionButton,
        body: safeBody,
      ),
    );
  }
}
