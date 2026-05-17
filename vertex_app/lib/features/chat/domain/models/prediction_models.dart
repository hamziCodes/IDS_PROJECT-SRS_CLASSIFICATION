class RequirementItem {
  RequirementItem({
    required this.text,
    required this.label,
    required this.confidence,
    required this.nfrTypes,
    required this.outlierProbability,
    required this.isOutlier,
  });

  final String text;
  final String label;
  final double? confidence;
  final List<String> nfrTypes;
  final double? outlierProbability;
  final bool isOutlier;

  factory RequirementItem.fromJson(Map<String, dynamic> json) {
    return RequirementItem(
      text: json['text'] as String? ?? '',
      label: json['label'] as String? ?? 'neither',
      confidence: (json['confidence'] as num?)?.toDouble(),
      nfrTypes: (json['nfr_types'] as List<dynamic>? ?? []).map((e) => e.toString()).toList(),
      outlierProbability: (json['outlier_probability'] as num?)?.toDouble(),
      isOutlier: json['is_outlier'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'text': text,
      'label': label,
      'confidence': confidence,
      'nfr_types': nfrTypes,
      'outlier_probability': outlierProbability,
      'is_outlier': isOutlier,
    };
  }
}

class PredictionResponse {
  PredictionResponse({
    required this.functionalRequirements,
    required this.nonFunctionalRequirements,
    required this.neither,
    required this.items,
    required this.counts,
  });

  final List<RequirementItem> functionalRequirements;
  final List<RequirementItem> nonFunctionalRequirements;
  final List<RequirementItem> neither;
  final List<RequirementItem> items;
  final Map<String, int> counts;

  factory PredictionResponse.fromJson(Map<String, dynamic> json) {
    return PredictionResponse(
      functionalRequirements: _parseItems(json['functional_requirements']),
      nonFunctionalRequirements: _parseItems(json['non_functional_requirements']),
      neither: _parseItems(json['neither']),
      items: _parseItems(json['items']),
      counts: (json['counts'] as Map<String, dynamic>? ?? {})
          .map((key, value) => MapEntry(key, (value as num).toInt())),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'functional_requirements': functionalRequirements.map((e) => e.toJson()).toList(),
      'non_functional_requirements': nonFunctionalRequirements.map((e) => e.toJson()).toList(),
      'neither': neither.map((e) => e.toJson()).toList(),
      'items': items.map((e) => e.toJson()).toList(),
      'counts': counts,
    };
  }

  static List<RequirementItem> _parseItems(dynamic raw) {
    final list = raw as List<dynamic>? ?? [];
    return list.map((item) => RequirementItem.fromJson(item as Map<String, dynamic>)).toList();
  }
}
