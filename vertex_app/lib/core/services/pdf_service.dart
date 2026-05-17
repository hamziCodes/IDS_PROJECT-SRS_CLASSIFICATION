import 'dart:io';
import 'dart:typed_data';

import 'package:intl/intl.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

import '../constants/app_constants.dart';
import '../../features/chat/domain/models/prediction_models.dart';

class PdfService {
  static Future<Uint8List> buildReport(PredictionResponse response) async {
    final doc = pw.Document();
    final now = DateTime.now();
    final formatter = DateFormat('MMM d, yyyy - HH:mm');

    doc.addPage(
      pw.MultiPage(
        pageTheme: pw.PageTheme(
          margin: const pw.EdgeInsets.all(36),
          theme: pw.ThemeData.withFont(
            base: pw.Font.helvetica(),
            bold: pw.Font.helveticaBold(),
          ),
        ),
        build: (context) => [
          _header(AppConstants.appName, AppConstants.reportTitle, formatter.format(now)),
          _section('Functional Requirements', response.functionalRequirements),
          _section('Non-Functional Requirements', response.nonFunctionalRequirements),
          _section('Neither Functional nor Non-Functional', response.neither),
        ],
      ),
    );

    return doc.save();
  }

  static Future<File> saveReport(Uint8List bytes) async {
    final dir = await getApplicationDocumentsDirectory();
    final stamp = DateFormat('yyyyMMdd_HHmmss').format(DateTime.now());
    final file = File('${dir.path}/vertex_report_$stamp.pdf');
    await file.writeAsBytes(bytes, flush: true);
    return file;
  }

  static pw.Widget _header(String brand, String title, String date) {
    return pw.Container(
      padding: const pw.EdgeInsets.only(bottom: 16),
      decoration: const pw.BoxDecoration(
        border: pw.Border(bottom: pw.BorderSide(width: 1, color: PdfColors.grey300)),
      ),
      child: pw.Row(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
        children: [
          pw.Column(
            crossAxisAlignment: pw.CrossAxisAlignment.start,
            children: [
              pw.Text(brand, style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold)),
              pw.SizedBox(height: 6),
              pw.Text(title, style: const pw.TextStyle(fontSize: 14)),
            ],
          ),
          pw.Text(date, style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700)),
        ],
      ),
    );
  }

  static pw.Widget _section(String title, List<RequirementItem> items) {
    return pw.Container(
      margin: const pw.EdgeInsets.only(top: 18),
      child: pw.Column(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.Text(title, style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold)),
          pw.SizedBox(height: 10),
          if (items.isEmpty)
            pw.Text('No entries in this section.', style: const pw.TextStyle(fontSize: 11, color: PdfColors.grey600))
          else
            pw.Column(
              children: items
                  .map(
                    (item) => pw.Padding(
                      padding: const pw.EdgeInsets.only(bottom: 8),
                      child: pw.Bullet(
                        text: item.text,
                        style: const pw.TextStyle(fontSize: 11),
                      ),
                    ),
                  )
                  .toList(),
            ),
        ],
      ),
    );
  }
}
