"""Phase 4.4: Cross-architecture convergence test.

Two-sample Kolmogorov-Smirnov test on vol spread distributions.
Gate A criterion: p < 0.10 (divergence) or p > 0.30 with similar medians (convergence).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, TypeAlias

import numpy as np
from numpy.typing import NDArray
from scipy.stats import ks_2samp

# Type aliases
FloatArray: TypeAlias = NDArray[np.float64]
ConvergenceClassification: TypeAlias = Literal["convergence", "divergence", "ambiguous"]

# Gate A thresholds
DIVERGENCE_P_THRESHOLD: Final[float] = 0.10
CONVERGENCE_P_THRESHOLD: Final[float] = 0.30
MEDIAN_RATIO_BOUNDS: Final[tuple[float, float]] = (0.5, 2.0)
MEDIAN_ABS_TOLERANCE: Final[float] = 0.05


@dataclass(frozen=True)
class ConvergenceResult:
    """Result of cross-architecture convergence test."""
    ks_statistic: float
    ks_pvalue: float
    bunni_median: float
    algebra_median: float
    bunni_mean: float
    algebra_mean: float
    bunni_std: float
    algebra_std: float
    bunni_n: int
    algebra_n: int


def run_convergence_test(
    bunni_vol_spreads: FloatArray,
    algebra_vol_spreads: FloatArray,
) -> ConvergenceResult:
    """Run two-sample KS test on vol spread distributions."""
    stat, pvalue = ks_2samp(bunni_vol_spreads, algebra_vol_spreads)
    return ConvergenceResult(
        ks_statistic=float(stat),
        ks_pvalue=float(pvalue),
        bunni_median=float(np.median(bunni_vol_spreads)),
        algebra_median=float(np.median(algebra_vol_spreads)),
        bunni_mean=float(np.mean(bunni_vol_spreads)),
        algebra_mean=float(np.mean(algebra_vol_spreads)),
        bunni_std=float(np.std(bunni_vol_spreads)),
        algebra_std=float(np.std(algebra_vol_spreads)),
        bunni_n=len(bunni_vol_spreads),
        algebra_n=len(algebra_vol_spreads),
    )


def classify_convergence(result: ConvergenceResult) -> ConvergenceClassification:
    """Classify convergence result per Gate A criteria."""
    if result.ks_pvalue < DIVERGENCE_P_THRESHOLD:
        return "divergence"
    if result.ks_pvalue > CONVERGENCE_P_THRESHOLD:
        if result.bunni_median > 0 and result.algebra_median > 0:
            ratio: float = result.bunni_median / result.algebra_median
            if MEDIAN_RATIO_BOUNDS[0] < ratio < MEDIAN_RATIO_BOUNDS[1]:
                return "convergence"
        elif abs(result.bunni_median - result.algebra_median) < MEDIAN_ABS_TOLERANCE:
            return "convergence"
    return "ambiguous"
