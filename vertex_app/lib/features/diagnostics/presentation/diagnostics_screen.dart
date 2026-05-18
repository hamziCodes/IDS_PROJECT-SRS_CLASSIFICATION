import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../../core/services/startup_log.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/widgets/app_drawer.dart';
import '../../../core/widgets/gradient_scaffold.dart';
import '../../../core/widgets/section_header.dart';
import '../../../core/widgets/vertex_app_bar.dart';

class DiagnosticsScreen extends StatefulWidget {
  const DiagnosticsScreen({super.key});

  @override
  State<DiagnosticsScreen> createState() => _DiagnosticsScreenState();
}

class _DiagnosticsScreenState extends State<DiagnosticsScreen> {
  @override
  Widget build(BuildContext context) {
    final logs = StartupLog.entries;

    return GradientScaffold(
      appBar: const VertexAppBar(showShare: false),
      drawer: const AppDrawer(),
      body: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        children: [
          const SectionHeader(
            title: 'Diagnostics',
            subtitle:
                'Startup logs and basic app state for black screen checks.',
          ),
          const SizedBox(height: 12),
          Card(
            color: AppColors.surface,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Logs', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 12),
                  if (logs.isEmpty)
                    Text(
                      'No startup logs captured yet.',
                      style: Theme.of(context).textTheme.bodyMedium,
                    )
                  else
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: logs
                          .map(
                            (log) => Padding(
                              padding: const EdgeInsets.only(bottom: 8),
                              child: SelectableText(
                                log,
                                style: Theme.of(context).textTheme.bodySmall,
                              ),
                            ),
                          )
                          .toList(),
                    ),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      TextButton.icon(
                        onPressed: () async {
                          await Clipboard.setData(
                            ClipboardData(text: logs.join('\n')),
                          );
                          if (!mounted) return;
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Logs copied')),
                          );
                        },
                        icon: const Icon(Icons.copy),
                        label: const Text('Copy logs'),
                      ),
                      TextButton.icon(
                        onPressed: () => setState(StartupLog.clear),
                        icon: const Icon(Icons.delete_outline),
                        label: const Text('Clear'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
