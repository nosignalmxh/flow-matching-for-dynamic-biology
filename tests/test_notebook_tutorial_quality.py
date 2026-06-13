from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

NOTEBOOKS = {
    "04_1_coupling_geometry.ipynb": {
        "min_code_cells": 24,
        "must_display": [
            "fig4_1_independent_coupling_paths.png",
            "fig4_2_random_vs_ot_pairs.png",
            "fig4_2b_epsilon_ablation_pairs.png",
            "fig4_3_reflow_representative_trajectories.png",
        ],
    },
    "04_2_state_space_representation_assumptions.ipynb": {
        "min_code_cells": 24,
        "must_display": [
            "fig4_5b_toy_branching_pairs.png",
            "fig4_8_toy_representation_couplings.png",
            "fig4_10_chord_vs_manifold_path.png",
            "fig4_10_eb_chord_vs_graph_path_phate.png",
        ],
    },
    "04_3_sampling_depth_and_claim_boundaries.ipynb": {
        "min_code_cells": 18,
        "must_display": [
            "plot_raw_observed_counts(",
            "plot_sampling_depth_bootstrap_sensitivity",
            "plot_stochastic_bridge_demo",
            "figA_4_1_prior_strength_sanity_check.png",
        ],
    },
    "05_2_perturbation_response_sciplex.ipynb": {
        "min_code_cells": 11,
        "must_display": [
            "fig_5_2_heldout_highest_dose_metrics",
            "fig_5_2_heldout_compound_metrics",
        ],
    },
}


def _payload(filename: str) -> dict:
    return json.loads((PROJECT_ROOT / "notebooks" / filename).read_text())


def _sources(filename: str, cell_type: str | None = None) -> list[str]:
    payload = _payload(filename)
    return [
        "".join(cell.get("source", []))
        for cell in payload["cells"]
        if cell_type is None or cell.get("cell_type") == cell_type
    ]


def test_tutorial_notebooks_have_stepwise_code_cells_and_compile():
    for filename, spec in NOTEBOOKS.items():
        code_sources = _sources(filename, "code")
        code_lengths = [source.count("\n") + bool(source) for source in code_sources]

        assert len(code_sources) >= spec["min_code_cells"], filename
        assert max(code_lengths) <= 100, (filename, max(code_lengths))

        for index, source in enumerate(code_sources, 1):
            compile(source, f"{filename}:code-cell-{index}", "exec")


def test_tutorial_notebooks_display_their_saved_figures_inline():
    for filename, spec in NOTEBOOKS.items():
        notebook_text = "\n".join(_sources(filename))
        code_text = "\n".join(_sources(filename, "code"))
        assert "from IPython.display import Image, display" in code_text, filename

        for figure_name in spec["must_display"]:
            assert figure_name in notebook_text, (filename, figure_name)

        display_markers = [
            "display(Image(",
            "display_saved_figure(",
            "display_saved_figures(",
            "display_figure(",
            "display_figure_output(",
            "display_png(",
        ]
        assert any(marker in code_text for marker in display_markers), filename


def test_tutorial_notebooks_keep_saved_output_references():
    for filename, spec in NOTEBOOKS.items():
        notebook_text = "\n".join(_sources(filename))
        code_text = "\n".join(_sources(filename, "code"))

        for figure_name in spec["must_display"]:
            assert figure_name in notebook_text, (filename, figure_name)

        output_guard_markers = [
            "raise FileNotFoundError",
            "resolve_required_artifact",
            "section52_required_paths",
            "display_saved_figure",
            "save_figure",
            "save_small_figure",
        ]
        assert any(marker in code_text for marker in output_guard_markers), filename
