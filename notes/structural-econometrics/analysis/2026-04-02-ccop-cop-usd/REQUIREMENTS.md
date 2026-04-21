# Analytics Reporter Code Requirements

## MANDATORY — all Python code in this directory must comply:

### 1. Dedicated Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install statsmodels pandas numpy scipy
```
All scripts run from this venv. No global pip installs.

### 2. Functional Programming Style
- Pure functions: data in → result out
- No global mutable state
- No classes with side effects
- All computations as callable, testable functions
- Side effects (file I/O, printing) isolated to main() only

### 3. TDD
- Tests alongside estimation code
- Test: merge row count
- Test: ln(1+V) handles zeros
- Test: quincena dummy fires on correct dates
- Test: decision rule matches pre-registered table

### 4. If the agent produced imperative code:
REFACTOR before running. The code must be functional and tested.
