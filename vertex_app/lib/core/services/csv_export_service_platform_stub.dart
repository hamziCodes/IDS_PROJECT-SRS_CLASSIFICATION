import 'csv_export_service.dart';

Future<CsvExportResult> saveCsvFile({required String fileName, required String csvContent}) async {
  return const CsvExportResult(message: 'CSV export is not supported on this platform.');
}
