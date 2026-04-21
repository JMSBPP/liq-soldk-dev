# Manual Data Step Required

The Dune API key is not available (free tier). The MCP tool retrieved all 499 rows but can't write them to disk programmatically.

## To get the data:

1. Open in browser: https://dune.com/queries/6941901
2. Click "Run" if needed (or results should be cached)
3. Click "Download CSV" button (available on free tier)
4. Save as: `notes/structural-econometrics/data/2026-04-02-ccop-cop-usd/raw/ccop_residual_daily.csv`

## Then run estimation:

```bash
cd /home/jmsbpp/apps/liq-soldk-dev/notes/structural-econometrics/analysis/2026-04-02-ccop-cop-usd
source .venv/bin/activate
python3 merge_and_estimate.py
```

## The estimation script expects either:
- `raw/ccop_residual_daily.csv` (CSV with header row)
- `raw/ccop_residual_daily.json` (JSON array of objects)

Both are handled by `load_onchain_from_dune_export()` in `merge_and_estimate.py`.
