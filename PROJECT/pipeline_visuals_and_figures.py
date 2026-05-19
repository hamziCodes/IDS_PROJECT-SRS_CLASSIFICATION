"""Generate report-ready visuals for the Vertex IDS pipeline.

This script creates figures for the IDS report:
- six-stage pipeline flow
- dataset row counts across stages
- model performance metrics
- NFR category distribution
- system architecture
- user flow

Run from the repository root:
    python PROJECT/pipeline_visuals_and_figures.py

Figures are saved to:
    .MD DOCS/report_figures/
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import scipy.sparse
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from pipeline_common import (
    MODEL_METADATA_PATH,
    NFR_TYPES,
    STAGE1_COMBINED_PATH,
    STAGE2_FILTERED_PATH,
    STAGE4_CLEANED_PATH,
    STAGE5_MATRIX_PATH,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / ".MD DOCS" / "report_figures"


STAGES = [
    {
        "id": "0",
        "title": "Outlier Training",
        "detail": "Learn junk/non-requirement patterns",
        "file": "0_Outlier_Training.py",
    },
    {
        "id": "1",
        "title": "Load + Merge",
        "detail": "Combine PROMISE + synthetic NFR data",
        "file": "1_Load_and_Merge.py",
    },
    {
        "id": "2",
        "title": "Outlier Gate",
        "detail": "Filter invalid requirement text",
        "file": "2_Outlier_Gate.py",
    },
    {
        "id": "3",
        "title": "EDA",
        "detail": "Study labels, overlap, and text length",
        "file": "3_EDA.py",
    },
    {
        "id": "4",
        "title": "Data Cleaning",
        "detail": "Normalize text for modeling",
        "file": "4_Data_Cleaning.py",
    },
    {
        "id": "5",
        "title": "Feature Engineering",
        "detail": "Convert text to TF-IDF vectors",
        "file": "5_Feature_Engineering.py",
    },
    {
        "id": "6",
        "title": "Training + Export",
        "detail": "Save classifiers and metadata",
        "file": "6_Model_Training_and_Export.py",
    },
]


def prepare_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "font.size": 10,
            "axes.titlesize": 14,
            "axes.labelsize": 10,
        }
    )


def read_row_count(path: Path) -> int | None:
    if not path.exists():
        return None
    return int(len(pd.read_csv(path)))


def load_metadata() -> dict:
    if MODEL_METADATA_PATH.exists():
        return joblib.load(MODEL_METADATA_PATH)
    return {}


def save_current_figure(name: str) -> None:
    path = OUTPUT_DIR / name
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


def add_box(
    ax,
    xy: tuple[float, float],
    width: float,
    height: float,
    title: str,
    subtitle: str = "",
    facecolor: str = "#1f2937",
    edgecolor: str = "#60a5fa",
    textcolor: str = "#f8fafc",
) -> None:
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.8,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    x, y = xy
    ax.text(
        x + width / 2,
        y + height * 0.62,
        title,
        ha="center",
        va="center",
        color=textcolor,
        weight="bold",
        fontsize=10,
    )
    if subtitle:
        ax.text(
            x + width / 2,
            y + height * 0.33,
            subtitle,
            ha="center",
            va="center",
            color="#cbd5e1",
            fontsize=8,
            wrap=True,
        )


def add_arrow(
    ax,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = "#94a3b8",
) -> None:
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=16,
        linewidth=1.8,
        color=color,
    )
    ax.add_patch(arrow)


def figure_pipeline_flow() -> None:
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 6)
    ax.axis("off")
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")

    ax.text(
        7.5,
        5.65,
        "Vertex IDS: Six-Stage Backend Pipeline",
        ha="center",
        va="center",
        color="#f8fafc",
        fontsize=18,
        weight="bold",
    )

    positions = [
        (0.4, 3.55),
        (2.45, 3.55),
        (4.5, 3.55),
        (6.55, 3.55),
        (8.6, 3.55),
        (10.65, 3.55),
        (12.7, 3.55),
    ]

    for i, stage in enumerate(STAGES):
        add_box(
            ax,
            positions[i],
            1.65,
            1.25,
            f"Stage {stage['id']}: {stage['title']}",
            stage["detail"],
            facecolor="#111827",
            edgecolor="#38bdf8",
        )
        ax.text(
            positions[i][0] + 0.825,
            positions[i][1] - 0.28,
            stage["file"],
            ha="center",
            color="#93c5fd",
            fontsize=7,
        )
        if i < len(positions) - 1:
            add_arrow(
                ax,
                (positions[i][0] + 1.67, positions[i][1] + 0.63),
                (positions[i + 1][0] - 0.05, positions[i + 1][1] + 0.63),
            )

    add_box(
        ax,
        (1.0, 1.0),
        2.5,
        1.0,
        "Raw + Augmented Data",
        "PROMISE dataset and synthetic NFR rows",
        facecolor="#064e3b",
        edgecolor="#34d399",
    )
    add_box(
        ax,
        (6.25, 1.0),
        2.5,
        1.0,
        "Cleaned Dataset",
        "Deduplicated and normalized text",
        facecolor="#312e81",
        edgecolor="#a78bfa",
    )
    add_box(
        ax,
        (11.45, 1.0),
        2.5,
        1.0,
        "Trained Artifacts",
        "Vectorizer, classifiers, labels, metadata",
        facecolor="#7c2d12",
        edgecolor="#fb923c",
    )
    add_arrow(ax, (3.5, 1.5), (6.15, 1.5), color="#cbd5e1")
    add_arrow(ax, (8.75, 1.5), (11.35, 1.5), color="#cbd5e1")

    save_current_figure("01_pipeline_flow.png")


def figure_stage_metrics() -> None:
    stage_counts = [
        ("Stage 1\nMerged", read_row_count(STAGE1_COMBINED_PATH)),
        ("Stage 2\nFiltered", read_row_count(STAGE2_FILTERED_PATH)),
        ("Stage 4\nCleaned", read_row_count(STAGE4_CLEANED_PATH)),
    ]
    df = pd.DataFrame(stage_counts, columns=["Stage", "Rows"]).dropna()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x="Stage", y="Rows", palette="viridis", ax=ax)
    ax.set_title("Dataset Size Across Pipeline Stages", weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Number of rows")
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=4)
    save_current_figure("02_stage_dataset_counts.png")


def figure_model_metrics() -> None:
    metadata = load_metadata()
    metrics = [
        ("FR/NFR\nAccuracy", metadata.get("accuracy_fr_nfr")),
        ("NFR Type\nAccuracy", metadata.get("accuracy_nfr_types")),
        ("NFR Weighted\nF1", metadata.get("weighted_f1_nfr_types")),
        ("NFR Hamming\nLoss", metadata.get("hamming_loss_nfr_types")),
    ]
    df = pd.DataFrame(metrics, columns=["Metric", "Value"]).dropna()
    df["Percent"] = df["Value"].astype(float) * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#2563eb", "#7c3aed", "#059669", "#dc2626"]
    sns.barplot(data=df, x="Metric", y="Percent", palette=colors[: len(df)], ax=ax)
    ax.set_title("Saved Model Performance Metrics", weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Value (%)")
    ax.set_ylim(0, max(100, float(df["Percent"].max()) + 8))
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f%%", padding=4)
    save_current_figure("03_model_metrics.png")


def figure_training_summary() -> None:
    metadata = load_metadata()
    values = {
        "Vocabulary\nSize": metadata.get("vocab_size"),
        "Total\nSamples": metadata.get("n_samples"),
        "Training\nSamples": metadata.get("n_train"),
        "Test\nSamples": metadata.get("n_test"),
    }
    df = pd.DataFrame(values.items(), columns=["Item", "Value"]).dropna()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x="Item", y="Value", palette="mako", ax=ax)
    ax.set_title("Training Dataset and Feature Summary", weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=4)
    save_current_figure("04_training_summary.png")


def figure_nfr_distribution() -> None:
    if not STAGE4_CLEANED_PATH.exists():
        print(f"Skipped NFR distribution; missing {STAGE4_CLEANED_PATH}")
        return

    df = pd.read_csv(STAGE4_CLEANED_PATH)
    counts = []
    for label in NFR_TYPES:
        if label in df.columns:
            counts.append((label, int(df[label].fillna(0).astype(int).sum())))

    if not counts:
        print("Skipped NFR distribution; no NFR columns found.")
        return

    plot_df = pd.DataFrame(counts, columns=["NFR Type", "Count"])
    plot_df = plot_df.sort_values("Count", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=plot_df, x="Count", y="NFR Type", palette="rocket", ax=ax)
    ax.set_title("NFR Category Distribution in Cleaned Dataset", weight="bold")
    ax.set_xlabel("Number of labeled rows")
    ax.set_ylabel("")
    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=4)
    save_current_figure("05_nfr_category_distribution.png")


def figure_feature_matrix() -> None:
    if not STAGE5_MATRIX_PATH.exists():
        print(f"Skipped feature matrix figure; missing {STAGE5_MATRIX_PATH}")
        return

    matrix = scipy.sparse.load_npz(STAGE5_MATRIX_PATH)
    rows, cols = matrix.shape
    non_zero = matrix.nnz
    total = rows * cols
    sparsity = 1 - non_zero / total

    labels = ["Non-zero\nTF-IDF values", "Zero values"]
    values = [non_zero, total - non_zero]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(
        values,
        labels=labels,
        autopct="%1.2f%%",
        startangle=90,
        colors=["#2563eb", "#e5e7eb"],
        textprops={"fontsize": 9},
    )
    ax.set_title(
        f"TF-IDF Matrix Sparsity\nShape: {rows} rows x {cols} features | Sparsity: {sparsity * 100:.2f}%",
        weight="bold",
    )
    save_current_figure("06_tfidf_matrix_sparsity.png")


def draw_flow_diagram(
    filename: str,
    title: str,
    nodes: Iterable[dict],
    arrows: Iterable[tuple[int, int]],
    size: tuple[int, int] = (12, 7),
) -> None:
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.text(6, 6.55, title, ha="center", color="#f8fafc", fontsize=17, weight="bold")

    node_list = list(nodes)
    for node in node_list:
        add_box(
            ax,
            node["xy"],
            node.get("w", 2.2),
            node.get("h", 0.9),
            node["title"],
            node.get("subtitle", ""),
            facecolor=node.get("color", "#111827"),
            edgecolor=node.get("edge", "#38bdf8"),
        )

    for source, target in arrows:
        source_node = node_list[source]
        target_node = node_list[target]
        sx = source_node["xy"][0] + source_node.get("w", 2.2)
        sy = source_node["xy"][1] + source_node.get("h", 0.9) / 2
        tx = target_node["xy"][0]
        ty = target_node["xy"][1] + target_node.get("h", 0.9) / 2
        add_arrow(ax, (sx, sy), (tx, ty))

    save_current_figure(filename)


def figure_system_architecture() -> None:
    nodes = [
        {
            "xy": (0.4, 4.8),
            "title": "Datasets",
            "subtitle": "PROMISE + synthetic NFR",
            "color": "#064e3b",
            "edge": "#34d399",
        },
        {
            "xy": (3.0, 4.8),
            "title": "Python IDS Pipeline",
            "subtitle": "clean, analyze, vectorize, train",
            "color": "#1e3a8a",
            "edge": "#60a5fa",
        },
        {
            "xy": (5.8, 4.8),
            "title": "Model Artifacts",
            "subtitle": "pkl, npy, metadata",
            "color": "#581c87",
            "edge": "#c084fc",
        },
        {
            "xy": (8.6, 4.8),
            "title": "FastAPI Backend",
            "subtitle": "Render deployment",
            "color": "#7c2d12",
            "edge": "#fb923c",
        },
        {
            "xy": (8.6, 2.5),
            "title": "Flutter App",
            "subtitle": "chat, model stats, export",
            "color": "#312e81",
            "edge": "#a78bfa",
        },
        {
            "xy": (5.8, 2.5),
            "title": "End User",
            "subtitle": "enters requirement text",
            "color": "#111827",
            "edge": "#facc15",
        },
    ]
    arrows = [(0, 1), (1, 2), (2, 3), (5, 4), (4, 3)]
    draw_flow_diagram("07_system_architecture.png", "System Architecture", nodes, arrows)


def figure_user_flow() -> None:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.text(6, 6.55, "User Flow: Requirement Classification", ha="center", color="#f8fafc", fontsize=17, weight="bold")

    boxes = [
        ((0.4, 5.0), "User Input", "Requirement text"),
        ((3.0, 5.0), "Flutter UI", "Send POST /predict"),
        ((5.6, 5.0), "FastAPI", "Validate request"),
        ((8.2, 5.0), "Preprocess", "clean + vectorize"),
        ((5.6, 3.1), "Outlier Gate", "valid requirement?"),
        ((8.2, 3.1), "FR/NFR Model", "functional or non-functional"),
        ((8.2, 1.2), "NFR Type Model", "multi-label categories"),
        ((3.0, 1.2), "Result Screen", "labels, confidence, stats"),
    ]

    for xy, title, subtitle in boxes:
        add_box(ax, xy, 2.1, 0.9, title, subtitle)

    arrows = [
        ((2.5, 5.45), (2.95, 5.45)),
        ((5.1, 5.45), (5.55, 5.45)),
        ((7.7, 5.45), (8.15, 5.45)),
        ((9.25, 5.0), (6.65, 4.0)),
        ((7.7, 3.55), (8.15, 3.55)),
        ((9.25, 3.1), (9.25, 2.1)),
        ((8.2, 1.65), (5.15, 1.65)),
    ]
    for start, end in arrows:
        add_arrow(ax, start, end)

    ax.text(4.9, 3.88, "if outlier: return Neither", color="#fca5a5", fontsize=9, ha="center")
    ax.text(10.25, 2.55, "if NFR", color="#bfdbfe", fontsize=9, ha="center")
    ax.text(6.65, 1.95, "JSON response", color="#cbd5e1", fontsize=9, ha="center")

    save_current_figure("08_user_flow.png")


def figure_backend_request_flow() -> None:
    nodes = [
        {"xy": (0.5, 4.8), "title": "POST /predict", "subtitle": "text + force_classify"},
        {"xy": (3.1, 4.8), "title": "schemas.py", "subtitle": "request validation"},
        {"xy": (5.7, 4.8), "title": "model_loader.py", "subtitle": "load cached artifacts"},
        {"xy": (8.3, 4.8), "title": "predictor.py", "subtitle": "run inference"},
        {
            "xy": (8.3, 2.5),
            "title": "Response JSON",
            "subtitle": "items, counts, labels",
            "color": "#064e3b",
            "edge": "#34d399",
        },
        {
            "xy": (5.7, 2.5),
            "title": "Flutter Parser",
            "subtitle": "PredictionResponse",
            "color": "#312e81",
            "edge": "#a78bfa",
        },
    ]
    arrows = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 4)]
    draw_flow_diagram("09_backend_request_flow.png", "Backend Request Flow", nodes, arrows)


def write_metrics_summary() -> None:
    metadata = load_metadata()
    rows = [
        ("Vocabulary Size", metadata.get("vocab_size", "N/A")),
        ("Total Samples", metadata.get("n_samples", "N/A")),
        ("Training Samples", metadata.get("n_train", "N/A")),
        ("Test Samples", metadata.get("n_test", "N/A")),
        ("FR/NFR Accuracy", metadata.get("accuracy_fr_nfr", "N/A")),
        ("NFR Type Accuracy", metadata.get("accuracy_nfr_types", "N/A")),
        ("NFR Weighted F1", metadata.get("weighted_f1_nfr_types", "N/A")),
        ("NFR Hamming Loss", metadata.get("hamming_loss_nfr_types", "N/A")),
    ]
    summary_path = OUTPUT_DIR / "metrics_summary.csv"
    pd.DataFrame(rows, columns=["Metric", "Value"]).to_csv(summary_path, index=False)
    print(f"Saved: {summary_path}")


def write_report_figure_index() -> None:
    lines = [
        "# Report Figure Index",
        "",
        "Use these generated figures in the IDS report.",
        "",
        "| Figure | File | Use in Report |",
        "|---|---|---|",
        "| 1 | `01_pipeline_flow.png` | Methodology / complete IDS pipeline |",
        "| 2 | `02_stage_dataset_counts.png` | Dataset processing and row counts |",
        "| 3 | `03_model_metrics.png` | Model results and evaluation |",
        "| 4 | `04_training_summary.png` | Training/test split and vocabulary size |",
        "| 5 | `05_nfr_category_distribution.png` | EDA / NFR label distribution |",
        "| 6 | `06_tfidf_matrix_sparsity.png` | Feature engineering / TF-IDF explanation |",
        "| 7 | `07_system_architecture.png` | Overall system architecture |",
        "| 8 | `08_user_flow.png` | User flow through the app and backend |",
        "| 9 | `09_backend_request_flow.png` | Backend API request lifecycle |",
        "",
        "Suggested Markdown insert format:",
        "",
        "```markdown",
        "![Pipeline Flow](report_figures/01_pipeline_flow.png)",
        "```",
        "",
    ]
    index_path = OUTPUT_DIR / "README_figures.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {index_path}")


def main() -> None:
    prepare_output_dir()
    figure_pipeline_flow()
    figure_stage_metrics()
    figure_model_metrics()
    figure_training_summary()
    figure_nfr_distribution()
    figure_feature_matrix()
    figure_system_architecture()
    figure_user_flow()
    figure_backend_request_flow()
    write_metrics_summary()
    write_report_figure_index()


if __name__ == "__main__":
    main()
