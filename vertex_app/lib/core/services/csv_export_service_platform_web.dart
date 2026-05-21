import 'dart:convert';
import 'dart:html' as html;

import 'csv_export_service.dart';

Future<CsvExportResult> saveCsvFile({required String fileName, required String csvContent}) async {
  final bytes = utf8.encode(csvContent);
  final blob = html.Blob([bytes], 'text/csv;charset=utf-8');
  final url = html.Url.createObjectUrlFromBlob(blob);

  final anchor = html.AnchorElement(href: url)
    ..download = fileName
    ..style.display = 'none';

  html.document.body?.append(anchor);
  anchor.click();
  anchor.remove();
  html.Url.revokeObjectUrl(url);

  return const CsvExportResult(message: 'CSV download started.');
}
