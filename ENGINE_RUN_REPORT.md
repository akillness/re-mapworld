# MapleSurvivalExpedition Engine Run Report

Generated: 2026-06-12

## Validation

```text
MSW script validation: PASS
Expanded balance evaluation: 7/7 criteria PASS
MSW Maker MCP build logs: 0 entries / 0 errors
```

Resource linkage validation: PASS (`docs/resource` 9 packets linked through map-attached `ExpeditionResourceCatalog`)

## Deterministic Gameplay Simulation

The local harness verifies the full 10-wave balance across 3 play policies and 3 seeds.

```json
{
  "all_passed": true,
  "criteria": {
    "AC2_standard_full_clear": true,
    "AC3_standard_session_length": true,
    "AC4_cautious_safe_extract": true,
    "AC5_greedy_risk_is_real": true,
    "AC6_difficulty_monotonic": true,
    "AC7_collection_discovery": true,
    "AC8_meta_settlement": true
  },
  "observed": {
    "standard_seconds": [556, 556, 556],
    "standard_outcomes": ["cleared", "cleared", "cleared"],
    "standard_collection": [7, 7, 7],
    "greedy_min_health": [0.251, 0.251, 0.251]
  }
}
```

## MSW Maker MCP setup

Official reference: <https://maplestoryworlds-creators.nexon.com/ko/docs?postId=1368>

- LocalWorkspace: enabled.
- ExtendedScriptFormat: enabled.
- Maker MCP transport: `stdio`.
- Actual launcher on this workstation: `D:\MapleStory Worlds\MakerMCP\msw-maker-mcp.bat`.
- Project config: `.mcp.json` and `.codex/config.toml`.
- API key policy: no literal key in repository; `msw-mcp` reads `MSW_MCP_API_KEY`.

`tools/list` returned 15 tools:

```text
maker_stop, maker_play, maker_refresh_workspace, maker_logs, maker_clear_logs,
maker_screenshot, maker_save, maker_get_current_map, maker_get_world_id,
maker_list_maplestory_maps, maker_get_context_keys, maker_execute_script,
maker_import_maplestory_map, maker_mouse_input, maker_keyboard_input
```

## MSW LocalWorkspace runtime script

Executable Maker-side validation code is in:

```text
RootDesk/MyDesk/MapleSurvivalExpedition/MapleSurvivalExpeditionRuntime.mlua
```

The script is a real `@Logic` loaded by MSW Maker. It runs an accelerated deterministic expedition that covers:

- 10 waves
- elite waves 3 / 6 / 9
- boss wave 10 (`BossBalrog`)
- monster collection entries
- level ups
- potion/food resource logic
- account-exp settlement

## MCP Play Test evidence

MCP sequence executed:

1. `maker_stop`
2. `maker_clear_logs`
3. `maker_refresh_workspace`
4. `maker_logs(kind="build")` → `count: 0`
5. `maker_play`
6. wait for runtime loop
7. `maker_logs(kind="normal")` → `count: 98`
8. `maker_get_context_keys` → `server_main`, `client`
9. `maker_execute_script(context="server_main")`
10. `maker_stop`, then new MCP session `maker_save` → `ok`

Runtime log tail:

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

Raw evidence: [`MSW_MCP_VERIFICATION.json`](MSW_MCP_VERIFICATION.json) and [`MSW_MCP_VERIFICATION.md`](MSW_MCP_VERIFICATION.md).

## Review-driven playable component verification

A follow-up review identified that the first MCP proof exercised an accelerated runtime harness, but did not prove the gameplay scripts were attached to map entities. The improvement pass added six map-attached gameplay entities:

```text
/maps/map01/BalanceTable           -> script.BalanceTable
/maps/map01/MonsterCollection      -> script.MonsterCollection
/maps/map01/PlayerSurvivalProbe    -> script.PlayerSurvivalStats
/maps/map01/MonsterSpawner         -> script.MonsterSpawner
/maps/map01/SurvivalHudBridge      -> script.SurvivalHudBridge
/maps/map01/SurvivalGameManager    -> script.SurvivalGameManager
```

MCP verification after the improvement:

```text
maker_stop
maker_clear_logs
maker_refresh_workspace
maker_logs(kind="build") -> count: 0
maker_play
maker_screenshot -> artifacts/msw_playable_entities_capture.png
maker_logs(kind="normal") -> count: 299
maker_execute_script(context="server_main")
maker_stop
maker_save -> ok
```

Positive runtime evidence:

```text
[MapleSurvivalExpedition][PLAYABLE] wave_clear wave=10 kills=7
[MapleSurvivalExpedition][PLAYABLE] expedition_complete outcome=cleared bossDefeated=true deaths=0 score=6320 accountExp=632 collection=7
[MapleSurvivalExpedition][PLAYABLE_QUERY] wave=10 outcome=cleared deaths=0 collection=7 accountExp=632
```

Raw evidence: [`MSW_PLAYABLE_REVIEW_VERIFICATION.json`](MSW_PLAYABLE_REVIEW_VERIFICATION.json) and [`MSW_PLAYABLE_REVIEW_VERIFICATION.md`](MSW_PLAYABLE_REVIEW_VERIFICATION.md).

## Ralph resource-linkage redo

The latest redo starts from the actual planning/resource folders under `docs/resource/` and binds them into the running map through:

```text
/maps/map01/ExpeditionResourceCatalog -> script.ExpeditionResourceCatalog
```

The catalog exposes Battle, Stage, Ranking, Miner growth, Monster Collection, Monster Book, Monster Dataset, UI, and Map packets. `SurvivalGameManager` now blocks startup if the catalog is missing and logs the source route used by every wave.

MCP sequence executed for this redo:

```text
maker_stop
maker_clear_logs
maker_refresh_workspace
maker_logs(kind="build") -> count: 0
maker_play
maker_screenshot -> artifacts/msw_resource_linked_ralph_capture.png
maker_logs(kind="normal") -> 311 logs
maker_get_context_keys -> server_main, client
maker_execute_script(context="server_main")
maker_logs(kind="normal") -> 312 logs including RESOURCE_QUERY
maker_stop
maker_save -> ok
maker_logs(kind="build") -> count: 0
```

Positive runtime evidence:

```text
[MapleSurvivalExpedition][RESOURCE] catalog_ready battleScripts=92 rankingScripts=8 stageScripts=6 minerPlayerScripts=68 collectionScripts=7 monsterBookScripts=3 monsterDatasets=9 ui=57 maps=44
[MapleSurvivalExpedition][RESOURCE] wave_route wave=10 packet=ranking-boss-settlement source=docs/resource/maple-soul-hero/scripts/Ranking/RankingLogic.mlua
[MapleSurvivalExpedition][PLAYABLE] expedition_complete outcome=cleared bossDefeated=true deaths=0 score=5596 accountExp=559 collection=7
[MapleSurvivalExpedition][RESOURCE_QUERY] wave=10 outcome=cleared complete=true resourceReady=true packets=battle,stage,ranking,miner,collection,book,dataset,ui,map wave10Source=docs/resource/maple-soul-hero/scripts/Ranking/RankingLogic.mlua
```

Raw evidence: [`RALPH_RESOURCE_LINKAGE_VERIFICATION.json`](RALPH_RESOURCE_LINKAGE_VERIFICATION.json), [`RESOURCE_LINKAGE_VERIFICATION.json`](RESOURCE_LINKAGE_VERIFICATION.json), and [`RALPH_RESOURCE_LINKAGE_VERIFICATION.md`](RALPH_RESOURCE_LINKAGE_VERIFICATION.md).

## Result

Static harness validation, deterministic balance simulation, official MSW Maker MCP connection, LocalWorkspace refresh, build-log inspection, Play Test execution, map-attached gameplay component execution, docs/resource packet linkage, runtime log verification, direct runtime state query, stop, and save are all verified.
