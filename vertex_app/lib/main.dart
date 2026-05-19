import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';
import 'core/services/startup_log.dart';

void main() {
  // 1. Catch Flutter UI framework errors and paint them to the screen
  FlutterError.onError = (FlutterErrorDetails details) {
    FlutterError.dumpErrorToConsole(details);
    runApp(
      ErrorScreen(
        error: details.exceptionAsString(),
        stackTrace: details.stack?.toString(),
      ),
    );
  };

  // 2. Catch asynchronous errors (like missing iOS permissions or failed async calls)
  runZonedGuarded<Future<void>>(
    () async {
      WidgetsFlutterBinding.ensureInitialized();
      StartupLog.add('WidgetsFlutterBinding.ensureInitialized() complete');

      await SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
      SystemChrome.setSystemUIOverlayStyle(
        const SystemUiOverlayStyle(
          statusBarColor: Colors.transparent,
          systemNavigationBarColor: Colors.transparent,
          systemNavigationBarDividerColor: Colors.transparent,
        ),
      );

      StartupLog.add('runApp() begin');
      runApp(const ProviderScope(child: VertexApp()));
    },
    (error, stack) {
      // Paint the error to the screen instead of silently crashing
      StartupLog.add('Uncaught zone error: $error');
      runApp(
        ErrorScreen(error: error.toString(), stackTrace: stack.toString()),
      );
    },
  );
}

/// A standalone, dependency-free screen that will pop up if the app crashes.
class ErrorScreen extends StatelessWidget {
  final String error;
  final String? stackTrace;

  const ErrorScreen({super.key, required this.error, this.stackTrace});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        backgroundColor: Colors.red.shade900,
        body: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '🚨 FATAL STARTUP ERROR 🚨',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  error,
                  style: const TextStyle(
                    color: Colors.yellow,
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 20),
                Text(
                  stackTrace ?? 'No stack trace provided.',
                  style: const TextStyle(color: Colors.white70, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
