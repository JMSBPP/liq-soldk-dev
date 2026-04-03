"""Phase 0: Bunni V2 pool inventory and LDF type identification.

Dune-first: query NewBunni events on Arbitrum to find all pools.
RPC fallback: read SSTORE2-packed PoolState to extract LDF address.
Match LDF address against known deployment addresses from contracts.json.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class PoolRecord:
    """A Bunni V2 pool discovered from NewBunni events."""
    bunni_token: str
    pool_id: str
    block_time: str
    tx_hash: str
    ldf_type: Optional[str] = None
    ldf_address: Optional[str] = None
    token0: Optional[str] = None
    token1: Optional[str] = None


def match_ldf_type(
    ldf_address: str,
    known_ldf_addresses: dict[str, str],
) -> Optional[str]:
    """Match an LDF contract address to a known LDF type.

    Args:
        ldf_address: The address to look up (lowercase hex, no checksum).
        known_ldf_addresses: Dict mapping ldf_type_name -> address.

    Returns:
        The LDF type name if matched, None otherwise.
    """
    normalized = ldf_address.lower()
    for ldf_name, addr in known_ldf_addresses.items():
        if addr.lower() == normalized:
            return ldf_name
    return None


def parse_new_bunni_event(log: dict) -> PoolRecord:
    """Parse a raw Dune log row for a NewBunni event.

    NewBunni(IBunniToken indexed bunniToken, PoolId indexed poolId)
    topic1 = bunniToken (address, left-padded to 32 bytes)
    topic2 = poolId (bytes32)
    """
    bunni_token = "0x" + log["topic1"][-40:]
    pool_id = log["topic2"]
    return PoolRecord(
        bunni_token=bunni_token,
        pool_id=pool_id,
        block_time=log.get("block_time", ""),
        tx_hash=log.get("tx_hash", ""),
    )


def classify_pools(
    pools: list[PoolRecord],
    target_ldf: str,
) -> list[PoolRecord]:
    """Filter pools to those matching the target LDF type."""
    return [p for p in pools if p.ldf_type == target_ldf]


def read_ldf_address_via_rpc(
    hub_address: str,
    pool_id: str,
    rpc_url: str,
) -> Optional[str]:
    """Read the LDF address from BunniHub storage via RPC.

    Uses `cast` (Foundry) to make the RPC call.
    Returns the LDF address or None if the call fails.
    """
    try:
        result = subprocess.run(
            [
                "cast", "call", hub_address,
                "poolState(bytes32)(address,bytes32,uint24,uint24,address,address)",
                pool_id,
                "--rpc-url", rpc_url,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split("\n")
            if lines:
                return lines[0].strip().lower()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def load_contracts() -> dict:
    """Load contract addresses from contracts.json."""
    return json.loads(Path("contracts.json").read_text())


def main() -> None:
    """Run Phase 0 feasibility check."""
    contracts = load_contracts()
    arb = contracts["bunni_v2"]["arbitrum"]
    ldf_addrs = arb["ldf"]

    print("Phase 0: Bunni V2 Pool Inventory on Arbitrum")
    print(f"Hub address: {arb['hub']}")
    print(f"GeometricDistribution address: {ldf_addrs['geometric']}")
    print()
    print("Step 1: Query Dune for NewBunni events...")
    print("Step 2: For each pool, read LDF address via RPC...")
    print("Step 3: Match LDF addresses against known deployments")
    print()
    print("GO/NO-GO: Need >= 3 GeometricDistribution pools with >= 5 completed lifecycles")


if __name__ == "__main__":
    main()
