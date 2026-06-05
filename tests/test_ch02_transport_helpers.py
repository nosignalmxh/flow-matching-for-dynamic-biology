from __future__ import annotations

import numpy as np


def test_median_positive_scale_ignores_zeros_and_falls_back_to_one():
    from src.ot import median_positive_scale

    C = np.asarray([[0.0, 2.0, 8.0], [0.0, 4.0, 0.0]], dtype=np.float32)
    assert median_positive_scale(C) == 4.0
    assert median_positive_scale(np.zeros((2, 2), dtype=np.float32)) == 1.0
