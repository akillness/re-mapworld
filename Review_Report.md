# Review Report: MapleStory Worlds Lua Scripts

## Scope

Reviewed MSW-ready scripts for the MapleSurvivalExpedition MVP:

- `PlayerSurvivalStats.lua`
- `MonsterSpawner.lua`
- `MonsterAgent.lua`
- `SurvivalGameManager.lua`
- `SurvivalHudBridge.lua`

## Findings

### PlayerSurvivalStats.lua

- Uses MSW `Property:` and `Method:` sections.
- Tracks synchronized health, hunger, level, experience, score, and death state.
- Hunger drains using `delta`, starvation damage is bounded by the death/reset flow, and level-up can process multiple level thresholds in one call.
- Result: ready for player entity attachment.

### MonsterSpawner.lua

- Uses wave-scaled spawn cap and spawn interval.
- Uses `_SpawnService:SpawnByModelId` with model ID, name, spawn position, parent, owner ID, and sync flags.
- Handles empty `MonsterModelId` as simulated/log-only spawn mode so Play can verify the loop before a real monster prefab is configured.
- Result: ready for spawn-point entity attachment.

### MonsterAgent.lua

- Implements monster health, attack ticks, damage, death logging, and `_EntityService:Destroy` cleanup.
- Result: ready for monster prefab attachment.

### SurvivalGameManager.lua

- Implements target waves, wave/rest state transitions, risk percentage, and expedition completion.
- Uses frame-rate independent `delta` timing.
- Result: ready as global logic.

### SurvivalHudBridge.lua

- Provides synchronized HUD text fields for wave, HP, hunger, risk, and victory state.
- Result: ready for UI binding once UI entities are created in Maker.

## Verification

Use the local project CLI:

```bash
python tools/msw_project_cli.py validate
python tools/msw_project_cli.py simulate --seconds 420
```

The latest generated run evidence is stored in `ENGINE_RUN_REPORT.md`.

## Conclusion

The project now has a complete MSW survival MVP script set plus a deterministic local validation/simulation harness. Engine launch is verified; direct MakerMCP injection is blocked by the current empty tool list and must be retried once MSW Maker exposes the editor bridge tools.
