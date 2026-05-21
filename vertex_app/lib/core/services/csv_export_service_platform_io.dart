import 'dart:io';
import 'dart:convert';

import 'package:path_provider/path_provider.dart';

import 'csv_export_service.dart';

Future<CsvExportResult> saveCsvFile({required String fileName, required String csvContent}) async {
  final dir = await getTemporaryDirectory();
  final file = File('${dir.path}/$fileName');
  await file.writeAsBytes(utf8.encode(csvContent), flush: true);
  return CsvExportResult(message: 'Saved to ${file.path}', filePath: file.path);
}
