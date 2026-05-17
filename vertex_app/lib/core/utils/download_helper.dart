import 'dart:convert';
import 'package:flutter/foundation.dart';

/// Platform-agnostic download helper
class DownloadHelper {
  static Future<void> downloadCsv(String csvContent, String filename) async {
    if (kIsWeb) {
      try {
        await _downloadWeb(csvContent, filename);
      } catch (e) {
        print('Web download error: $e');
        rethrow;
      }
    } else {
      // Mobile and desktop platforms need file_saver or similar setup
      await _downloadNative(csvContent, filename);
    }
  }

  static Future<void> _downloadWeb(String csvContent, String filename) async {
    // For web, we use a workaround with data URLs
    final bytes = utf8.encode(csvContent);
    final base64Str = base64Encode(bytes);
    final dataUrl = 'data:text/csv;base64,$base64Str';

    // We'll use JavaScript interop to trigger the download
    _triggerWebDownload(dataUrl, filename);
  }

  static void _triggerWebDownload(String dataUrl, String filename) {
    // Note: This requires dart:html to be imported separately for web
    // In your main app, ensure this works with proper context
    try {
      // Using a simple approach with HTML
      final code =
          '''
        var link = document.createElement('a');
        link.href = '$dataUrl';
        link.download = '$filename';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      ''';

      // For now, we'll just print - you need to integrate with js interop properly
      print('Download triggered for: $filename');
    } catch (e) {
      print('Error triggering download: $e');
    }
  }

  static Future<void> _downloadNative(
    String csvContent,
    String filename,
  ) async {
    // For mobile/desktop, you would use file_saver or similar package
    // This is a placeholder - implement based on your needs
    print('Native download for: $filename - not yet implemented');
  }
}
