"""Tests for Phase 0 feasibility checks."""
from dataclasses import dataclass
import json
from pathlib import Path

from phase0_feasibility import (
    match_ldf_type,
    parse_new_bunni_event,
    classify_pools,
    PoolRecord,
)


def test_match_ldf_type_geometric() -> None:
    """Known geometric address maps to 'geometric'."""
    contracts = json.loads(Path("contracts.json").read_text())
    ldf_addrs = contracts["bunni_v2"]["arbitrum"]["ldf"]
    result = match_ldf_type(ldf_addrs["geometric"], ldf_addrs)
    assert result == "geometric"


def test_match_ldf_type_unknown() -> None:
    """Unknown address returns None."""
    contracts = json.loads(Path("contracts.json").read_text())
    ldf_addrs = contracts["bunni_v2"]["arbitrum"]["ldf"]
    result = match_ldf_type("0x0000000000000000000000000000000000000000", ldf_addrs)
    assert result is None


def test_parse_new_bunni_event() -> None:
    """Synthetic NewBunni event log decodes correctly."""
    fake_log = {
        "topic1": "0x000000000000000000000000aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "topic2": "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "block_time": "2025-03-15T12:00:00",
        "tx_hash": "0xcccc",
    }
    record = parse_new_bunni_event(fake_log)
    assert record.bunni_token == "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert record.pool_id == "0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"


def test_classify_pools_filters_geometric() -> None:
    """classify_pools keeps only geometric pools."""
    pools = [
        PoolRecord(bunni_token="0xaaa", pool_id="0x111", block_time="2025-03-15", tx_hash="0xfff", ldf_type="geometric"),
        PoolRecord(bunni_token="0xbbb", pool_id="0x222", block_time="2025-03-16", tx_hash="0xeee", ldf_type="uniform"),
        PoolRecord(bunni_token="0xccc", pool_id="0x333", block_time="2025-03-17", tx_hash="0xddd", ldf_type=None),
    ]
    result = classify_pools(pools, target_ldf="geometric")
    assert len(result) == 1
    assert result[0].pool_id == "0x111"
