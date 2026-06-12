# Review-Driven Playable Verification

Generated: 2026-06-12

This pass addressed the review finding that the previous evidence proved a runtime harness but did not prove map-attached gameplay components. The world now includes map entities that attach the playable scripts directly through `map/map01.map`.

## Map-attached gameplay entities

| Entity path | Script component |
|---|---|
| `/maps/map01/BalanceTable` | `script.BalanceTable` |
| `/maps/map01/MonsterCollection` | `script.MonsterCollection` |
| `/maps/map01/PlayerSurvivalProbe` | `script.PlayerSurvivalStats` |
| `/maps/map01/MonsterSpawner` | `script.MonsterSpawner` |
| `/maps/map01/SurvivalHudBridge` | `script.SurvivalHudBridge` |
| `/maps/map01/SurvivalGameManager` | `script.SurvivalGameManager` |

## MCP verification sequence

1. `maker_stop` → edit mode.
2. `maker_clear_logs` → isolated current run.
3. `maker_refresh_workspace` → LocalWorkspace synced.
4. `maker_logs(kind="build")` → `count: 0`, `logs: []`.
5. `maker_play` → Play mode started.
6. `maker_screenshot` → `artifacts/msw_playable_entities_capture.png`.
7. `maker_logs(kind="normal")` → 299 runtime logs.
8. `maker_execute_script(context="server_main")` → queried live map component state.
9. `maker_stop` and `maker_save` → saved verified world state.

## Positive checks

| Check | Result |
|---|---|
| Build log count is zero | PASS |
| `BalanceTable` map component attached | PASS |
| `MonsterCollection` map component attached | PASS |
| `MonsterSpawner` map component attached | PASS |
| `PlayerSurvivalStats` map probe attached | PASS |
| `SurvivalGameManager` map component attached | PASS |
| Wave 10 started | PASS |
| BossBalrog spawned | PASS |
| BossBalrog registered as collection entry 7 | PASS |
| Expedition completed with `outcome=cleared` | PASS |

## Runtime evidence tail

```text
[MapleSurvivalExpedition][PLAYABLE] spawn monster=BossBalrog wave=10 risk=62
[MapleSurvivalExpedition][PLAYABLE] defeat_resolved monster=BossBalrog score=5120 health=203
[MapleSurvivalExpedition][PLAYABLE] defeat monster=BossBalrog wave=10 kills=5
[MapleSurvivalExpedition][PLAYABLE] spawn monster=BossBalrog wave=10 risk=76
[MapleSurvivalExpedition][PLAYABLE] defeat_resolved monster=BossBalrog score=5720 health=196
[MapleSurvivalExpedition][PLAYABLE] defeat monster=BossBalrog wave=10 kills=6
[MapleSurvivalExpedition][PLAYABLE] spawn monster=BossBalrog wave=10 risk=91
[MapleSurvivalExpedition][PLAYABLE] level_up level=7 score=6320
[MapleSurvivalExpedition][PLAYABLE] defeat_resolved monster=BossBalrog score=6320 health=228
[MapleSurvivalExpedition][PLAYABLE] defeat monster=BossBalrog wave=10 kills=7
[MapleSurvivalExpedition][PLAYABLE] wave_clear wave=10 kills=7
[MapleSurvivalExpedition][PLAYABLE] expedition_complete outcome=cleared bossDefeated=true deaths=0 score=6320 accountExp=632 collection=7
```

Direct live query:

```text
[MapleSurvivalExpedition][PLAYABLE_QUERY] wave=10 outcome=cleared deaths=0 collection=7 accountExp=632
```

Machine-readable evidence: [`MSW_PLAYABLE_REVIEW_VERIFICATION.json`](MSW_PLAYABLE_REVIEW_VERIFICATION.json).
