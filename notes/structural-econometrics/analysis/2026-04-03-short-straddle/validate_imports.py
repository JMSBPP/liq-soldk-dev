#!/usr/bin/env python
"""Validate that modules import without errors."""
from __future__ import annotations

import sys

try:
    import convergence
    print("✓ convergence.py imports successfully")
    print(f"  - ConvergenceResult: {convergence.ConvergenceResult}")
    print(f"  - test_convergence: {convergence.test_convergence}")
    print(f"  - classify_convergence: {convergence.classify_convergence}")
except Exception as e:
    print(f"✗ convergence.py import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    import test_convergence
    print("✓ test_convergence.py imports successfully")
    print(f"  - test_convergence_identical_distributions: {test_convergence.test_convergence_identical_distributions}")
    print(f"  - test_convergence_different_distributions: {test_convergence.test_convergence_different_distributions}")
    print(f"  - test_convergence_ambiguous: {test_convergence.test_convergence_ambiguous}")
except Exception as e:
    print(f"✗ test_convergence.py import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAll imports successful!")
