# MSW Maker MCP Verification

Generated: 2026-06-12

Official setup reference: <https://maplestoryworlds-creators.nexon.com/ko/docs?postId=1368>

## MCP configuration

- LocalWorkspace: enabled in MSW Maker AI ToolKit.
- ExtendedScriptFormat: enabled in MSW Maker AI ToolKit.
- Maker MCP transport: `stdio`.
- Actual launcher on this workstation: `D:\MapleStory Worlds\MakerMCP\msw-maker-mcp.bat`.
- Project config: `.mcp.json` (`msw-maker-mcp`, `msw-mcp`, `ouroboros`) and `.codex/config.toml`.
- API key handling: `msw-mcp` uses `${MSW_MCP_API_KEY}` / `bearer_token_env_var = "MSW_MCP_API_KEY"`; no literal API key is stored in the repo.

## Tool discovery

`tools/list` returned 15 Maker tools:

```text
maker_stop
maker_play
maker_refresh_workspace
maker_logs
maker_clear_logs
maker_screenshot
maker_save
maker_get_current_map
maker_get_world_id
maker_list_maplestory_maps
maker_get_context_keys
maker_execute_script
maker_import_maplestory_map
maker_mouse_input
maker_keyboard_input
```

## Runtime script under LocalWorkspace

MSW Maker exported the world into this project folder. The executable validation script is:

```text
RootDesk/MyDesk/MapleSurvivalExpedition/MapleSurvivalExpeditionRuntime.mlua
```

Maker refresh generated:

```text
RootDesk/MyDesk/MapleSurvivalExpedition/MapleSurvivalExpeditionRuntime.codeblock
```

## Verification sequence

MCP calls executed:

1. `maker_stop` → `already_stopped`, mode `edit`.
2. `maker_clear_logs` → cleared previous logs.
3. `maker_refresh_workspace` → `ok`.
4. `maker_logs(kind="build")` → `count: 0`, `logs: []`.
5. `maker_play` → `ok`, mode `edit_to_play`.
6. wait for accelerated runtime validation to finish.
7. `maker_logs(kind="normal")` → `count: 98`.
8. `maker_get_context_keys` → `server_main`, `client`.
9. `maker_execute_script(context="server_main", ...)` queried runtime state directly.
10. `maker_stop` → edit mode; follow-up session `maker_save` → `ok`.

## Positive runtime evidence

Build logs:

```json
{"status":"ok","kind":"build","count":0,"logs":[]}
```

Runtime checks:

| Check | Result |
|---|---|
| Runtime script entered `OnBeginPlay` | PASS |
| Wave 10 boss wave started | PASS |
| Boss forecast emitted | PASS |
| Expedition completed | PASS |
| Deaths stayed zero | PASS |
| Monster collection reached 7 entries | PASS |

Tail evidence from Maker runtime logs:

```text
[MapleSurvivalExpedition][MCP] wave_start wave=10 type=boss duration=3.0
[MapleSurvivalExpedition][MCP] boss forecast: BossBalrog is entering wave 10
[MapleSurvivalExpedition][MCP] collection_add monster=BossBalrog count=7
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=2818 health=174 risk=7
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=3418 health=169 risk=22
[MapleSurvivalExpedition][MCP] level_up level=13 score=4018
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=4018 health=180 risk=37
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=4618 health=173 risk=52
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=5218 health=166 risk=68
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=5818 health=159 risk=83
[MapleSurvivalExpedition][MCP] level_up level=14 score=6418
[MapleSurvivalExpedition][MCP] defeat monster=BossBalrog wave=10 score=6418 health=180 risk=98
[MapleSurvivalExpedition][MCP] wave_clear wave=10 kills=7 health=180
[MapleSurvivalExpedition][MCP] expedition_complete outcome=cleared bossDefeated=true deaths=0 score=6418 accountExp=641 collection=7
```

Direct runtime query via `maker_execute_script`:

```text
[MapleSurvivalExpedition][MCP_QUERY] wave=10 outcome=cleared deaths=0 collection=7 accountExp=641
```

Raw machine-readable evidence: [`MSW_MCP_VERIFICATION.json`](MSW_MCP_VERIFICATION.json).
