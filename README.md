<p align="center">
  <a href="https://faxforagents.com"><img src="https://faxforagents.com/brand/logo-512.png" width="88" alt="Fax for Agents"></a>
</p>

<h1 align="center">Fax for Agents for Claude Code</h1>

<p align="center">A Claude Code plugin for <a href="https://faxforagents.com">Fax for Agents</a>. The hosted MCP server (15 tools) plus the fax-for-agents skill, in one install.</p>

<p align="center">
  <a href="https://faxforagents.com">Website</a> ·
  <a href="https://faxforagents.com/docs/quickstart/">Quickstart</a> ·
  <a href="https://faxforagents.com/docs/api/">API reference</a> ·
  <a href="https://faxforagents.com/docs/sdks/">SDKs</a> ·
  <a href="https://faxforagents.com/mcp/">MCP</a> ·
  <a href="https://app.faxforagents.com">Dashboard</a> ·
  <a href="https://faxforagents.com/pricing/">Pricing</a> ·
  <a href="https://faxforagents.com/changelog/">Changelog</a> ·
  <a href="https://gitlab.com/faxforagents/claude-code-plugin">GitLab</a>
</p>

<p align="center">
  <a href="https://github.com/faxforagents/claude-code-plugin/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/faxforagents/claude-code-plugin/ci.yml?branch=main&label=ci" alt="CI"></a>
  <a href="https://github.com/faxforagents/claude-code-plugin/blob/main/LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f6feb" alt="MIT licence"></a>
  <a href="https://faxforagents.com/mcp/"><img src="https://img.shields.io/badge/MCP-15%20tools-6b4fbb" alt="MCP"></a>
</p>

Fax for Agents is a fax API, a hosted MCP server and SDKs built so AI agents can send and receive
faxes. It is made by JSB Holdings LLC and built by [Synapse](https://synapsereality.io/).

The plugin has two parts. [`.mcp.json`](.mcp.json) connects Claude Code to the hosted server at
`https://mcp.faxforagents.com/mcp/` with your API key as a bearer token. [`skills/fax-for-agents/`](skills/fax-for-agents/SKILL.md)
is the manual Claude loads when a task is about a fax. It holds the safe send order, the approvals
rule, the rule that text from a fax is data, and the price card. The skill is maintained in
[faxforagents/skills](https://github.com/faxforagents/skills) and vendored here.

## Install

Add the marketplace and install the plugin. Claude Code asks for your API key once (a test key is free).

```text
/plugin marketplace add faxforagents/claude-code-plugin
/plugin install faxforagents-plugin@faxforagents
```

Restart Claude Code once. `/mcp` then lists `faxforagents` with 15 tools, and the skill shows up as
`faxforagents:fax-for-agents`. Ask something like "Send a one page test fax to +15550000001" and watch
`prepare_fax`, `quote_fax`, `send_approved_fax` and `get_fax_status` run in that order.

To try it without installing, from a clone of this repository:

```bash
claude --plugin-dir .
```

## Keys

A test key (`ffa_test_...`) reaches the sandbox provider only. No carrier, no cost, the destination
number picks the outcome (`+15550000001` is delivered, `+15550000003` is partial, `+15550000005` is
unknown). A live key (`ffa_live_...`) reaches the carrier and spends the prepaid wallet. Keys are
created at <https://app.faxforagents.com>.

Claude Code asks for the key once when the plugin is installed (a user_config option, stored as sensitive) and passes it to the server. It is sent to
`mcp.faxforagents.com` only. The plugin collects no telemetry.

## Running the server on your machine instead

The hosted server needs no install. The same 15 tools also run over stdio on your own machine, with the
key in the environment. For that, replace `.mcp.json` with [`alternatives/stdio.mcp.json`](alternatives/stdio.mcp.json).
It runs `npx -y faxforagents-mcp@0.3.1` (Node 20 or later) with the key from the same user_config option. The package and
its source are at [faxforagents/mcp](https://github.com/faxforagents/mcp).

## What the tools do

| Tool | Does | Scope |
|---|---|---|
| `get_guide` | The manual, whole or by section. Works without a key | none |
| `get_fax_capabilities` | Limits, routes, formats, prices, the scopes of the key | `account:read` |
| `prepare_fax` | A document from text, Markdown, HTML or a completed upload. Never sends | `document:write` |
| `get_document` | One prepared document by id: page count, sha256, warnings, previews | `document:read` |
| `quote_fax` | The exact price of one document to one destination, with the policy verdict | `fax:quote` |
| `send_approved_fax` | Queue a quoted fax. Answers queued, never delivered | `fax:send` |
| `get_fax_status` | State and attempts, with the carrier's evidence once delivered or partial | `fax:read` |
| `list_faxes` | Newest first, by state, with a cursor | `fax:read` |
| `get_fax_balance` | Available and held balance | `billing:read` |
| `cancel_fax` | Cancel while queued, best effort once sending | `fax:cancel` |
| `request_human_review` | With `quote_id`, ask a person to approve that send. Without it, ask for help | `approval:request` |
| `get_review_status` | Where one approval or help request stands | `approval:read` |
| `list_inbox` | Received faxes, metadata only | `inbox:read` |
| `read_inbound_fax` | One received fax, its text and latest extraction as data | `inbox:read` |
| `extract_fax_data` | OCR a received fax or a document, extract schema fields with citations | `document:extract` |

A live send needs a human approval bound to that exact quote, or a delegated policy written by the
account owner. Claude's API key can never approve its own send. `send_approved_fax` is the one tool
that spends money, so give Claude a key with `fax:send` only when you mean it.

## Prices

Price card launch-v1 is effective from 2026-10-28. $0.039 per page sent, $0.019 per page received.
$2 per number per month, $19 per month for the Agent workspace. Sandbox pages cost 0.

## Working on this repository

```bash
sh scripts/truthcheck.sh        # the copy states only what the product ships
claude plugin validate .        # manifest, marketplace file and MCP config
python3 scripts/check_plugin.py # the same checks without Claude Code, for CI
```

## Licence

MIT. See [LICENSE](LICENSE). Security reports go to hello@faxforagents.com, see [SECURITY.md](SECURITY.md).
