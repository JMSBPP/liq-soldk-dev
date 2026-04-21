"""
Extract Dune query results via pagination and save as CSVs.
Uses the Dune API via subprocess calls to the MCP.

This is a helper script — the actual extraction will be done
by paginating through mcp__dune__getExecutionResults in the main process.
"""
# This file documents the extraction methodology.
# Actual extraction is done via MCP tool calls in the Claude session.
# See queries.md for query IDs and URLs.
