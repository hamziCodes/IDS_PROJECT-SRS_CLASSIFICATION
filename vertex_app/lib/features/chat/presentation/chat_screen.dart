import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:share_plus/share_plus.dart';

import '../../../core/services/haptic_service.dart';
import '../../../core/services/pdf_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/widgets/app_drawer.dart';
import '../../../core/widgets/gradient_scaffold.dart';
import '../../../core/widgets/section_header.dart';
import '../../../core/widgets/vertex_app_bar.dart';
import '../domain/models/prediction_models.dart';
import 'controller/chat_controller.dart';
import 'widgets/chat_input_bar.dart';
import 'widgets/message_list.dart';
import 'widgets/pdf_share_sheet.dart';

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _handleSend() async {
    await HapticService.mediumImpact();
    final text = _controller.text;
    _controller.clear();
    await ref.read(chatControllerProvider.notifier).sendMessage(text);
    _scrollToBottom();
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 200), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent + 120,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _openShareSheet(PredictionResponse response) async {
    if (kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('PDF export is not available on web yet.'),
        ),
      );
      return;
    }
    if (!mounted) return;
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (_) => PdfShareSheet(
        onShare: () async {
          Navigator.of(context).pop();
          final bytes = await PdfService.buildReport(response);
          final file = await PdfService.saveReport(bytes);
          await Share.shareXFiles([
            XFile(file.path),
          ], text: 'Vertex classification report');
        },
        onDownload: () async {
          Navigator.of(context).pop();
          final bytes = await PdfService.buildReport(response);
          final file = await PdfService.saveReport(bytes);
          if (!mounted) return;
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('Saved to ${file.path}')));
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(chatControllerProvider);
    final lastPrediction = state.lastPrediction;
    final isIOS = !kIsWeb && defaultTargetPlatform == TargetPlatform.iOS;

    return GradientScaffold(
      appBar: VertexAppBar(
        showShare: true,
        onShare: lastPrediction == null
            ? null
            : () => _openShareSheet(lastPrediction),
      ),
      drawer: const AppDrawer(),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16),
            child: SectionHeader(
              title: 'Try out our model',
              subtitle:
                  'Paste software requirements and let Vertex classify them instantly.',
            ),
          ),
          Expanded(child: MessageList(scrollController: _scrollController)),
          Padding(
            padding: EdgeInsets.fromLTRB(16, 0, 16, isIOS ? 24 : 16),
            child: ChatInputBar(
              controller: _controller,
              isLoading: state.isLoading,
              onSend: _handleSend,
            ),
          ),
          if (state.errorMessage != null)
            Padding(
              padding: const EdgeInsets.only(left: 16, right: 16, bottom: 12),
              child: Row(
                children: [
                  const Icon(
                    Icons.warning_amber_rounded,
                    color: AppColors.warning,
                    size: 18,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      state.errorMessage!,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(
                        context,
                      ).textTheme.bodySmall?.copyWith(color: AppColors.warning),
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
