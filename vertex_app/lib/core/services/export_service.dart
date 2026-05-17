import 'dart:convert';
import 'package:csv/csv.dart';
import '../../features/chat/domain/models/prediction_models.dart';

class ExportService {
  /// Generates CSV content from prediction results
  static String generateCsv(PredictionResponse prediction) {
    final List<List<String>> csvData = [];

    // Add header row
    csvData.add(['requirement_text', 'classified_as', 'sub_category']);

    // Process Functional Requirements
    for (final item in prediction.functionalRequirements) {
      csvData.add([item.text, 'FR', 'N/A']);
    }

    // Process Non-Functional Requirements
    for (final item in prediction.nonFunctionalRequirements) {
      final subCategory = item.nfrTypes.isNotEmpty
          ? item.nfrTypes.join(', ')
          : 'N/A';
      csvData.add([item.text, 'NFR', subCategory]);
    }

    // Process Neither
    for (final item in prediction.neither) {
      csvData.add([item.text, 'Neither', 'N/A']);
    }

    // Convert to CSV format
    return const ListToCsvConverter().convert(csvData);
  }

  /// Generates filename with timestamp
  static String generateFilename() {
    final now = DateTime.now();
    final timestamp =
        '${now.year}${now.month.toString().padLeft(2, '0')}${now.day.toString().padLeft(2, '0')}_${now.hour.toString().padLeft(2, '0')}${now.minute.toString().padLeft(2, '0')}';
    return 'requirements_classification_$timestamp.csv';
  }

  /// Converts CSV string to bytes (UTF-8)
  static List<int> getCsvBytes(String csvContent) {
    return utf8.encode(csvContent);
  }
}
