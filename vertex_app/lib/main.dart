import 'dart:async';
import 'package:flutter/material.dart';

void main() {
  // Catch any framework errors
  FlutterError.onError = (FlutterErrorDetails details) {
    FlutterError.dumpErrorToConsole(details);
  };

  // Run a completely stripped-down app
  runZonedGuarded<Future<void>>(
    () async {
      WidgetsFlutterBinding.ensureInitialized();

      // Removed all SystemChrome awaits!
      // Removed Riverpod!
      // Removed VertexApp!

      runApp(
        const MaterialApp(
          debugShowCheckedModeBanner: false,
          home: Scaffold(
            backgroundColor: Colors.green,
            body: Center(
              child: Text(
                "IT LIVES!",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
      );
    },
    (error, stack) {
      debugPrint('Uncaught error: $error');
    },
  );
}
