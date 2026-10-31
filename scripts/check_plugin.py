#!/usr/bin/env python3
"""Check the plugin files without Claude Code installed: valid JSON, the required fields, the vendored skill.

Standard library only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    problems: list[str] = []
    plugin = load(".claude-plugin/plugin.json")
    for field in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords"):
        if field not in plugin:
            problems.append(f"plugin.json: {field} is missing")
    if plugin.get("name") != "faxforagents":
        problems.append("plugin.json: name must be faxforagents")
    market = load(".claude-plugin/marketplace.json")
    for field in ("name", "owner", "plugins"):
        if field not in market:
            problems.append(f"marketplace.json: {field} is missing")
    entries = market.get("plugins", [])
    if len(entries) != 1 or entries[0].get("source") != "./" or entries[0].get("name") != plugin.get("name"):
        problems.append("marketplace.json: one entry named like the plugin with source ./")
    mcp = load(".mcp.json")
    server = mcp.get("mcpServers", {}).get("faxforagents", {})
    if server.get("url") != "https://mcp.faxforagents.com/mcp/":
        problems.append(".mcp.json: the hosted server url must be https://mcp.faxforagents.com/mcp/")
    if "${FAXFORAGENTS_API_KEY}" not in json.dumps(server):
        problems.append(".mcp.json: the key must come from ${FAXFORAGENTS_API_KEY}")
    stdio = load("alternatives/stdio.mcp.json")["mcpServers"]["faxforagents"]
    if stdio.get("args") != ["-y", "faxforagents-mcp"]:
        problems.append("alternatives/stdio.mcp.json: args must be -y faxforagents-mcp")
    skill = ROOT / "skills" / "fax-for-agents" / "SKILL.md"
    if not skill.is_file() or not skill.read_text(encoding="utf-8").startswith("---\nname: fax-for-agents\n"):
        problems.append("skills/fax-for-agents/SKILL.md is missing or its frontmatter does not start with the name")
    for problem in problems:
        print(f"check_plugin: FAIL: {problem}", file=sys.stderr)
    if not problems:
        print("check_plugin: OK")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
