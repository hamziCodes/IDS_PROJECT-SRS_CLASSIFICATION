class StartupLog {
  static final List<String> _entries = <String>[];

  static List<String> get entries => List<String>.unmodifiable(_entries);

  static void add(String message) {
    final timestamp = DateTime.now().toIso8601String();
    final entry = '[$timestamp] $message';
    _entries.add(entry);
    if (_entries.length > 120) {
      _entries.removeRange(0, _entries.length - 120);
    }
  }

  static void clear() {
    _entries.clear();
  }
}
