import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../features/about/presentation/about_screen.dart';
import '../features/chat/presentation/chat_screen.dart';
import '../features/diagnostics/presentation/diagnostics_screen.dart';
import '../features/model/presentation/model_screen.dart';
import '../features/splash/presentation/splash_screen.dart';

CustomTransitionPage<void> _fadeTransition(Widget child) {
  return CustomTransitionPage<void>(
    child: child,
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      return FadeTransition(opacity: animation, child: child);
    },
  );
}

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      pageBuilder: (context, state) => _fadeTransition(const SplashScreen()),
    ),
    GoRoute(
      path: '/home',
      pageBuilder: (context, state) => _fadeTransition(const ChatScreen()),
    ),
    GoRoute(
      path: '/model',
      pageBuilder: (context, state) => _fadeTransition(const ModelScreen()),
    ),
    GoRoute(
      path: '/about',
      pageBuilder: (context, state) => _fadeTransition(const AboutScreen()),
    ),
    GoRoute(
      path: '/diagnostics',
      pageBuilder: (context, state) =>
          _fadeTransition(const DiagnosticsScreen()),
    ),
  ],
);
