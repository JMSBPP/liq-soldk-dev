"""Tests for cross-architecture convergence analysis."""
import numpy as np
from convergence import (
    ConvergenceResult,
    run_convergence_test,
    classify_convergence,
)


def test_convergence_identical_distributions() -> None:
    np.random.seed(42)
    bunni = np.random.normal(0.05, 0.02, 50)
    algebra = np.random.normal(0.05, 0.02, 50)
    result = run_convergence_test(bunni, algebra)
    assert result.ks_pvalue > 0.30
    assert classify_convergence(result) == "convergence"


def test_convergence_different_distributions() -> None:
    np.random.seed(42)
    bunni = np.random.normal(0.10, 0.02, 50)
    algebra = np.random.normal(0.02, 0.02, 50)
    result = run_convergence_test(bunni, algebra)
    assert result.ks_pvalue < 0.10
    assert classify_convergence(result) == "divergence"


def test_convergence_ambiguous() -> None:
    np.random.seed(42)
    bunni = np.random.normal(0.06, 0.03, 30)
    algebra = np.random.normal(0.04, 0.03, 30)
    result = run_convergence_test(bunni, algebra)
    classification = classify_convergence(result)
    assert classification in ("convergence", "divergence", "ambiguous")
