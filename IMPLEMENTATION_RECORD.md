# MapleSurvivalExpedition Implementation Record

## 2026-06-12 — Official MSW Maker MCP verification

### Completed

- Followed the official MSW MCP guide (`postId=1368`): LocalWorkspace and ExtendedScriptFormat were enabled in Maker; `.mcp.json` and `.codex/config.toml` were sanitized to use `MSW_MCP_API_KEY` instead of a literal API key.
- Verified `msw-maker-mcp` over stdio from the project folder using the actual workstation launcher `D:\MapleStory Worlds\MakerMCP\msw-maker-mcp.bat`.
- `tools/list` returned 15 Maker tools (`maker_refresh_workspace`, `maker_play`, `maker_logs`, `maker_execute_script`, etc.).
- Added executable LocalWorkspace runtime logic: `RootDesk/MyDesk/MapleSurvivalExpedition/MapleSurvivalExpeditionRuntime.mlua`.
- Ran the official MCP verification loop: `maker_stop` → `maker_clear_logs` → `maker_refresh_workspace` → `maker_logs(kind="build")` → `maker_play` → `maker_logs(kind="normal")` → `maker_execute_script` → `maker_stop` → `maker_save`.
- Evidence:
  - Build logs: `count=0`.
  - Runtime logs: 98 entries.
  - Completion log: `expedition_complete outcome=cleared bossDefeated=true deaths=0 score=6418 accountExp=641 collection=7`.
  - Runtime query log: `wave=10 outcome=cleared deaths=0 collection=7 accountExp=641`.
- Added `MSW_MCP_VERIFICATION.md` and `MSW_MCP_VERIFICATION.json`.

## 2026-06-11 — Balance & content expansion (ralph loop)

### Completed

- Registered the ouroboros MCP server in `.mcp.json` (`ouroboros mcp serve`, 23 `ouroboros_*` tools verified) for ralph subagent execution.
- Expanded content to the full contest design from `docs/join_develop.md`:
  - 10-wave expedition (normal x6 / elite x3 / boss x1), 7 monster types, risk-gauge scaling.
  - Consumables (potion/food drops, auto-use), rest-phase campfire healing, starvation.
  - Escape decision window after each wave (extract = keep 100%, wipe = keep 40%).
  - Monster collection (도감) with permanent attack/health bonuses (`MonsterCollection.lua`).
  - Account meta settlement (score -> account exp).
  - Data-driven balance: `balance_table.json` SSOT -> generated `BalanceTable.lua` (`gen-lua`).
- Extended the harness: `expedition`, `evaluate` (7 acceptance criteria, 3 policies x 3 seeds), `balance-loop` (auto-tuner with diagnosis, criteria-count-first acceptance, plateau kicks), `charts`.
- Ran the ralph loop 260+ iterations across 4 rounds (60/60/60/80). Structural fixes between rounds: rest-phase healing, elite-once-per-wave, kill-speed diagnosis, plateau escape kicks. Final round: **7/7 criteria PASS** (fitness 7.95/8.0).
- Verified balance: standard full-clears boss in 556s (~9.3 min, inside the 5-12 min design window) with 0 deaths; cautious extracts safely; greedy dips to 25.1% health (risk is real); difficulty monotonic; 7/7 monster types discovered.
- Delivery: README rewritten with shields.io badges, game introduction, banner (`artifacts/banner.png`), balance charts (`artifacts/balance_progression.png`, `artifacts/wave_difficulty.png`), engine screenshots; planning docs committed under `docs/` (heavy upstream resources gitignored).

## 2026-06-11

### Completed

- Built the MSW script set for a complete survival-expedition MVP:
  - `PlayerSurvivalStats.lua`
  - `MonsterSpawner.lua`
  - `MonsterAgent.lua`
  - `SurvivalGameManager.lua`
  - `SurvivalHudBridge.lua`
- Added `project_manifest.json` to describe attachment points, acceptance checks, and engine integration.
- Added `tools/msw_project_cli.py`, an agent-native CLI harness for this project.
- Added deterministic simulation coverage for the full five-wave expedition loop.
- Added MakerMCP probing and MSW Maker process launch verification.

### Engine integration findings

- `D:/MapleStory Worlds/msw.exe` is installed and can be launched.
- `D:/MapleStory Worlds/MakerMCP/MakerMCP.exe` initializes over JSON-RPC.
- `tools/list` currently returns an empty tool array in this session, so direct MCP-based scene/script injection is blocked until the Maker editor bridge exposes tools.
- The implementation is therefore delivered as MSW-ready scripts plus a validation/run harness and a reproducible engine launch report.

### Acceptance criteria evidence

Run these commands from `C:/Users/bangg/MapleSurvivalExpedition`:

```bash
python tools/msw_project_cli.py validate
python tools/msw_project_cli.py simulate --seconds 420
python tools/msw_project_cli.py launch-engine
python tools/msw_project_cli.py maker-status
python tools/msw_project_cli.py write-run-report
```

The generated `ENGINE_RUN_REPORT.md` records the current outputs.
