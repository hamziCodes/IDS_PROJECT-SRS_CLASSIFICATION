import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/widgets/app_drawer.dart';
import '../../../core/widgets/gradient_scaffold.dart';
import '../../../core/widgets/section_header.dart';
import '../../../core/widgets/vertex_app_bar.dart';
import '../../../core/widgets/glass_container.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return GradientScaffold(
      appBar: const VertexAppBar(showShare: false),
      drawer: const AppDrawer(),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SectionHeader(
              title: 'About Vertex',
              subtitle:
                  'A startup building intelligent systems for the next decade.',
            ),
            const SizedBox(height: 12),
            GlassContainer(
              child: Text(
                'Vertex is a research-driven startup focused on AI, ML, NLP, and intelligent systems. '
                'We build decision-grade models that turn raw data into clear, operational insights.',
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ),
            const SizedBox(height: 18),
            const SectionHeader(title: 'What We Do'),
            _pillRow(context, [
              'AI',
              'ML',
              'NLP',
              'Data Science',
              'Intelligent Systems',
            ]),
            const SizedBox(height: 18),
            const SectionHeader(title: 'Contact'),
            GlassContainer(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _infoRow(context, 'Email', 'vertex11solution@gmail.com'),
                  _infoRow(
                    context,
                    'Website',
                    'https://vertex-devsolutions.vercel.app/',
                  ),
                  // LinkedIn links
                  _infoRow(
                    context,
                    'LinkedIn (Hamza)',
                    'https://www.linkedin.com/in/hamzasultan-dev/',
                  ),
                  _infoRow(
                    context,
                    'LinkedIn (Shahzaib)',
                    'https://www.linkedin.com/in/shahzaib-farooq-/',
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _pillRow(BuildContext context, List<String> items) {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: items
          .map(
            (item) => Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: AppColors.surfaceSoft,
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(item, style: Theme.of(context).textTheme.bodyMedium),
            ),
          )
          .toList(),
    );
  }

  Widget _infoRow(BuildContext context, String label, String value) {
    final isLink =
        value.startsWith('http://') ||
        value.startsWith('https://') ||
        value.contains('@');

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 4),
          if (isLink)
            GestureDetector(
              onTap: () => _launchUrl(value),
              child: Text(
                value,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Colors.blue,
                  decoration: TextDecoration.underline,
                ),
              ),
            )
          else
            Text(
              value,
              style: Theme.of(
                context,
              ).textTheme.bodyMedium?.copyWith(color: AppColors.textSecondary),
            ),
        ],
      ),
    );
  }

  Future<void> _launchUrl(String urlString) async {
    final url = urlString.contains('@')
        ? Uri(scheme: 'mailto', path: urlString)
        : Uri.parse(urlString);

    if (await canLaunchUrl(url)) {
      await launchUrl(url);
    } else {
      debugPrint('Could not launch $url');
    }
  }
}
