class ModelInfo {
  ModelInfo({
    required this.modelName,
    required this.version,
    required this.metrics,
    required this.nfrTypes,
    required this.metadata,
  });

  final String modelName;
  final String version;
  final Map<String, dynamic> metrics;
  final List<String> nfrTypes;
  final Map<String, dynamic> metadata;

  factory ModelInfo.fromJson(Map<String, dynamic> json) {
    return ModelInfo(
      modelName: json['model_name'] as String? ?? 'Vertex Model',
      version: json['version'] as String? ?? '1.0.0',
      metrics: (json['metrics'] as Map<String, dynamic>? ?? {}),
      nfrTypes: (json['nfr_types'] as List<dynamic>? ?? []).map((e) => e.toString()).toList(),
      metadata: (json['metadata'] as Map<String, dynamic>? ?? {}),
    );
  }
}
