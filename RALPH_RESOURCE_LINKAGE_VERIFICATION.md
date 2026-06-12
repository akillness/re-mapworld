# Ralph Resource Linkage Verification

Generated: 2026-06-12

## Scope

This pass restarted the delivery loop from the actual planning/resource packet instead of treating the prior gameplay harness as enough. The world now includes a map-attached `ExpeditionResourceCatalog` component that exposes the real planning script/resource sources under `docs/resource/` to the running MSW Maker world, and `SurvivalGameManager` refuses to run if that catalog is missing or incomplete.

## Linked source packets

| Packet | Source path | Count | Runtime role |
|---|---|---:|---|
| Battle | `docs/resource/maple-soul-hero/scripts/Battle` | 92 `.mlua` | elite-wave combat event reference |
| Stage | `docs/resource/maple-soul-hero/scripts/Stage` | 6 `.mlua` | stage entry / wave transition reference |
| Ranking | `docs/resource/maple-soul-hero/scripts/Ranking` | 8 `.mlua` | wave-10 boss settlement / ranking reference |
| Miner growth | `docs/resource/miner-simulator/scripts/Components/Player` | 68 `.mlua` | repeat-session resource growth reference |
| Monster collection | `docs/resource/monster-farm/scripts/Collection` | 7 `.mlua` | collection and reward reference |
| Monster book | `docs/resource/monster-farm/scripts/Book` | 3 `.mlua` | monster-book reward flow reference |
| Monster dataset | `docs/resource/monster-farm/datasets/DataSet/Monster` | 9 `.csv` | monster base data reference |
| UI | `docs/resource/maple-soul-hero/ui` | 57 `.ui` | battle/ranking/status UI source packet |
| Maps | `docs/resource/miner-simulator/maps` | 44 `.map` | expanded expedition-area map packet |

## Runtime integration

Added:

```text
/maps/map01/ExpeditionResourceCatalog -> script.ExpeditionResourceCatalog
```

`SurvivalGameManager` now checks the catalog on `OnBeginPlay`, logs the linked packet list, and logs one source route per wave:

```text
wave=1  -> monster-dataset       -> docs/resource/monster-farm/datasets/DataSet/Monster/MonsterDataSet_Base.csv
wave=2  -> stage-entry           -> docs/resource/maple-soul-hero/scripts/Stage/Logic/StageLogic.mlua
wave=3  -> battle-elite-wave     -> docs/resource/maple-soul-hero/scripts/Battle/Event/WaveStartEvent.mlua
wave=4  -> miner-resource-growth -> docs/resource/miner-simulator/scripts/Components/Player/Accessory/PlayerAccessory.mlua
wave=5  -> monster-collection    -> docs/resource/monster-farm/scripts/Collection/CollectionService.mlua
wave=6  -> battle-elite-wave     -> docs/resource/maple-soul-hero/scripts/Battle/Event/WaveStartEvent.mlua
wave=7  -> miner-resource-growth -> docs/resource/miner-simulator/scripts/Components/Player/Accessory/PlayerAccessory.mlua
wave=8  -> monster-collection    -> docs/resource/monster-farm/scripts/Collection/CollectionService.mlua
wave=9  -> battle-elite-wave     -> docs/resource/maple-soul-hero/scripts/Battle/Event/WaveStartEvent.mlua
wave=10 -> ranking-boss-settlement -> docs/resource/maple-soul-hero/scripts/Ranking/RankingLogic.mlua
```

## Maker MCP sequence

Executed against the real MapleStory Worlds Maker window through `D:/MapleStory Worlds/MakerMCP/MakerMCP.exe` JSON-RPC:

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
maker_save
maker_logs(kind="build") -> count: 0
```

## Positive evidence

```text
[MapleSurvivalExpedition][RESOURCE] catalog linked packets=battle,stage,ranking,miner,collection,book,dataset,ui,map
[MapleSurvivalExpedition][RESOURCE] catalog_ready battleScripts=92 rankingScripts=8 stageScripts=6 minerPlayerScripts=68 collectionScripts=7 monsterBookScripts=3 monsterDatasets=9 ui=57 maps=44
[MapleSurvivalExpedition][RESOURCE] source book=docs/resource/monster-farm/scripts/Book/Logic/BookService.mlua
[MapleSurvivalExpedition][RESOURCE] wave_route wave=10 packet=ranking-boss-settlement source=docs/resource/maple-soul-hero/scripts/Ranking/RankingLogic.mlua
[MapleSurvivalExpedition][PLAYABLE] expedition_complete outcome=cleared bossDefeated=true deaths=0 score=5596 accountExp=559 collection=7
[MapleSurvivalExpedition][RESOURCE_QUERY] wave=10 outcome=cleared complete=true resourceReady=true packets=battle,stage,ranking,miner,collection,book,dataset,ui,map wave10Source=docs/resource/maple-soul-hero/scripts/Ranking/RankingLogic.mlua
```

## Harness evidence

```bash
python tools/msw_project_cli.py validate
python tools/msw_project_cli.py evaluate
python tools/msw_project_cli.py resource-linkage
```

All three passed. `resource-linkage --json` produced [`RESOURCE_LINKAGE_VERIFICATION.json`](RESOURCE_LINKAGE_VERIFICATION.json), and the full Maker MCP proof is summarized in [`RALPH_RESOURCE_LINKAGE_VERIFICATION.json`](RALPH_RESOURCE_LINKAGE_VERIFICATION.json).

## Result

The from-scratch ralph redo is verified: resource packets exist, the catalog is attached to the actual map, build logs are clean, Maker Play runs, wave routes reference the real planning/resource files, direct runtime query confirms `resourceReady=true`, and the 10-wave expedition clears in the engine.
