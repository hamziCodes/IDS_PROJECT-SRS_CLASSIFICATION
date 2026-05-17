// This file provides web-specific download functionality
// It's only imported/used on web platform

import 'dart:js' as js;
import 'dart:convert';

class WebDownloadUtil {
  /// Triggers a CSV download in the browser
  static void downloadCsv(String csvContent, String filename) {
    late String dataUrl;
    try {
      final bytes = utf8.encode(csvContent);
      final base64String = base64Encode(bytes);
      dataUrl = 'data:text/csv;base64,$base64String';

      // Create and trigger download via JavaScript
      js.context.callMethod('eval', [
        '''
        (function() {
          var link = document.createElement('a');
          link.href = '$dataUrl';
          link.download = '$filename';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        })();
        ''',
      ]);
    } catch (e) {
      print('Download error: $e');
      _fallbackDownload(dataUrl, filename);
    }
  }

  static void _fallbackDownload(String dataUrl, String filename) {
    try {
      // Alternative approach using window.open
      js.context.callMethod('open', [dataUrl]);
    } catch (e) {
      print('Fallback download failed: $e');
    }
  }
}
