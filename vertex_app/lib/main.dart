import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';
import 'core/services/startup_log.dart';

void main() {
  // Lightweight startup logging to help diagnose startup issues on devices.
  StartupLog.add('main() start');
  debugPrint('Vertex: main() start');

  // Forward Flutter framework errors to the console and to the zone handler.
  FlutterError.onError = (FlutterErrorDetails details) {
    FlutterError.dumpErrorToConsole(details);
    StartupLog.add('FlutterError: ${details.exception}');
  };

  // Run the app inside a guarded zone to capture uncaught async errors.
  runZonedGuarded<Future<void>>(
    () async {
      WidgetsFlutterBinding.ensureInitialized();
      StartupLog.add('WidgetsFlutterBinding.ensureInitialized() complete');

      StartupLog.add('runApp() begin');
      debugPrint('VertexApp: starting');
      runApp(const ProviderScope(child: VertexApp()));
      StartupLog.add('runApp() invoked');
    },
    (error, stack) {
      // Keep this lightweight — only log errors. Do not change app flow.
      StartupLog.add('Uncaught zone error: $error');
      debugPrint('VertexApp: Uncaught zone error: $error');
      if (stack != null) debugPrint(stack.toString());
    },
  );
}
