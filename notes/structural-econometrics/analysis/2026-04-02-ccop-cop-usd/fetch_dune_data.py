"""Fetch all rows from Dune query #6941901 via paginated API calls and save as JSON."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

QUERY_ID = 6941901
API_KEY = os.environ.get("DUNE_API_KEY", "")
# If not set, try reading from ~/.claude.json MCP config
if not API_KEY:
    try:
        import json as _json
        with open(os.path.expanduser("~/.claude.json")) as _f:
            _config = _json.load(_f)
        for _name, _srv in _config.get("mcpServers", {}).items():
            if "dune" in _name.lower():
                _headers = _srv.get("headers", {})
                for _k, _v in _headers.items():
                    if "api" in _k.lower() and "key" in _k.lower():
                        API_KEY = _v
                        break
                if not API_KEY:
                    _env = _srv.get("env", {})
                    API_KEY = _env.get("DUNE_API_KEY", "")
                if API_KEY:
                    break
    except Exception:
        pass
BASE_URL = f"https://api.dune.com/api/v1/query/{QUERY_ID}/results"
OUTPUT = Path(__file__).parent.parent.parent / "data" / "2026-04-02-ccop-cop-usd" / "raw" / "ccop_residual_daily.json"

def fetch_page(offset: int, limit: int = 100) -> list[dict]:
    url = f"{BASE_URL}?limit={limit}&offset={offset}"
    req = urllib.request.Request(url, headers={"X-DUNE-API-KEY": API_KEY})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data.get("result", {}).get("rows", [])

def main():
    if not API_KEY:
        print("Set DUNE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    all_rows = []
    offset = 0
    while True:
        rows = fetch_page(offset)
        if not rows:
            break
        all_rows.extend(rows)
        print(f"Fetched {len(rows)} rows (total: {len(all_rows)})")
        offset += len(rows)
        time.sleep(1)  # rate limit courtesy

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(all_rows, f, indent=2)
    print(f"Saved {len(all_rows)} rows to {OUTPUT}")

if __name__ == "__main__":
    main()
