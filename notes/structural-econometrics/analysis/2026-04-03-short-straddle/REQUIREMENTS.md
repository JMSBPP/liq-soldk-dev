# Short Straddle Analysis Code Requirements

## MANDATORY — all Python code in this directory must comply:

### 1. Dedicated Virtual Environment
All scripts run from `.venv`. No global pip installs.

### 2. Functional Programming Style
- Pure functions: data in -> result out
- No global mutable state
- No classes with side effects
- All computations as callable, testable functions
- Side effects (file I/O, printing, Dune API calls) isolated to main() only
- Use frozen dataclasses for structured data (PositionRecord, FitResult, etc.)

### 3. TDD
- Tests alongside analysis code
- Every pure function has at least one test
- Test with known synthetic data before real data

### 4. Dune Queries
- All queries must be permanent (saved, not temp)
- Record query ID and URL in this file when created
- Never use temporary query execution

### Query Registry
| Query ID | Description | URL |
|---|---|---|
| TBD | Bunni V2 pool inventory (Arbitrum) | TBD |
| TBD | Bunni V2 deposits/withdrawals (Arbitrum) | TBD |
| TBD | Bunni V2 swap events (Arbitrum) | TBD |
| TBD | Algebra Camelot positions (Arbitrum) | TBD |
| TBD | Algebra Camelot swap events (Arbitrum) | TBD |
