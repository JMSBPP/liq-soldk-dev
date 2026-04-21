#!/usr/bin/env python
"""Simple test runner for convergence tests."""
from __future__ import annotations

import sys
import traceback
from typing import Callable

# Import test functions
from test_convergence import (
    test_convergence_identical_distributions,
    test_convergence_different_distributions,
    test_convergence_ambiguous,
)

# Test registry
TESTS: dict[str, Callable[[], None]] = {
    "test_convergence_identical_distributions": test_convergence_identical_distributions,
    "test_convergence_different_distributions": test_convergence_different_distributions,
    "test_convergence_ambiguous": test_convergence_ambiguous,
}


def run_tests() -> int:
    """Run all tests and return exit code."""
    passed = 0
    failed = 0

    for test_name, test_func in TESTS.items():
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            traceback.print_exc()
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
