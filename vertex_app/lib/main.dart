import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';

void main() {
  // Lightweight startup logging to help diagnose startup issues on devices
  // These prints will appear in device logs and TestFlight diagnostics.
  print('Vertex: main() start');

  WidgetsFlutterBinding.ensureInitialized();

  // Forward Flutter framework errors to the console and to the zone handler.
  FlutterError.onError = (FlutterErrorDetails details) {
    FlutterError.dumpErrorToConsole(details);
  };

  // Run the app inside a guarded zone to capture uncaught async errors.
  runZonedGuarded<Future<void>>(
    () async {
      debugPrint('VertexApp: starting');
      runApp(const ProviderScope(child: VertexApp()));
    },
    (error, stack) {
      // Keep this lightweight — only log errors. Do not change app flow.
      debugPrint('VertexApp: Uncaught zone error: $error');
      if (stack != null) debugPrint(stack.toString());
    },
  );
}
