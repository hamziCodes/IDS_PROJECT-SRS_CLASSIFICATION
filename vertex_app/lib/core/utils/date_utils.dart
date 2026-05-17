import 'package:intl/intl.dart';

class DateUtilsX {
  static String formatDateTime(DateTime value) {
    return DateFormat('MMM d, yyyy - HH:mm').format(value);
  }
}
