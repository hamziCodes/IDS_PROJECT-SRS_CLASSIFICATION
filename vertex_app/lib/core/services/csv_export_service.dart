import '../../features/chat/domain/models/prediction_models.dart';
import 'csv_export_service_platform.dart' as platform;

class CsvExportResult {
  const CsvExportResult({required this.message, this.filePath});

  final String message;
  final String? filePath;
}

class CsvExportService {
  static String buildClassificationCsv(PredictionResponse response) {
    final rows = <List<String>>[
      const ['requirement_text', 'classified_as', 'sub_category'],
    ];

    rows.addAll(
      response.functionalRequirements.map(
        (item) => [item.text, 'FR', 'N/A'],
      ),
    );

    rows.addAll(
      response.nonFunctionalRequirements.map(
        (item) => [item.text, 'NFR', item.nfrTypes.isEmpty ? 'N/A' : item.nfrTypes.join(' | ')],
      ),
    );

    rows.addAll(
      response.neither.map(
        (item) => [item.text, 'Neither', 'N/A'],
      ),
    );

    return rows.map(_toCsvLine).join('\n');
  }

  static Future<CsvExportResult> saveClassificationCsv(String csvContent) {
    final stamp = DateTime.now().millisecondsSinceEpoch;
    final fileName = 'vertex_classification_$stamp.csv';
    return platform.saveCsvFile(fileName: fileName, csvContent: csvContent);
  }

  static String _toCsvLine(List<String> cells) {
    return cells.map(_escapeCell).join(',');
  }

  static String _escapeCell(String value) {
    final escaped = value.replaceAll('"', '""');
    return '"$escaped"';
  }
}
