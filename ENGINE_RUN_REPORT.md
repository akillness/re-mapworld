# MapleSurvivalExpedition Engine Run Report

Generated: 2026-06-11

## Validation

```text
MSW script validation: PASS
```

## Deterministic Gameplay Simulation

```json
{
  "ok": true,
  "seconds_requested": 420,
  "seconds_simulated": 415,
  "completed_at": 415.0,
  "player": {
    "health": 240.0,
    "hunger": 122.4,
    "level": 8,
    "exp": 270,
    "score": 3070,
    "deaths": 0
  },
  "game": {
    "wave": 5,
    "complete": true,
    "risk_percent": 100.0
  },
  "spawner": {
    "total_spawned": 74,
    "alive": 0
  },
  "event_count": 157,
  "events_tail": [
    {"time": 388, "event": "monster_defeated", "wave": 5, "level": 8},
    {"time": 390, "event": "spawn", "wave": 5, "alive": 1},
    {"time": 392, "event": "monster_defeated", "wave": 5, "level": 8},
    {"time": 395, "event": "spawn", "wave": 5, "alive": 1},
    {"time": 396, "event": "monster_defeated", "wave": 5, "level": 8},
    {"time": 400, "event": "spawn", "wave": 5, "alive": 1},
    {"time": 400, "event": "monster_defeated", "wave": 5, "level": 8},
    {"time": 405, "event": "spawn", "wave": 5, "alive": 1},
    {"time": 408, "event": "monster_defeated", "wave": 5, "level": 8},
    {"time": 410, "event": "spawn", "wave": 5, "alive": 1},
    {"time": 412, "event": "monster_defeated", "wave": 5, "level": 8},
    {"time": 415, "event": "complete", "wave": 5}
  ]
}
```

## MSW Maker Launch and Play Preview

- MSW executable: `D:\MapleStory Worlds\msw.exe`
- MSW Maker process: running.
- World template: created from scratch/basic MSW template.
- Created world name: `MapleSurvivalExpedition`.
- Created MSW component resource visible in Workspace: `PlayerSurvivalStats`.
- Play Preview: started successfully with green Play state and live player character visible.
- Evidence screenshot: `artifacts/msw_after_f5.png` and `artifacts/msw_play_started.png`.

## MakerMCP Probe

```json
{
  "ok": true,
  "mcp_initialized": true,
  "tools_available": 0,
  "tools": [],
  "note": "MakerMCP initializes, but the editor bridge exposed no tools in this session. GUI execution was used instead."
}
```

## Result

Static validation, deterministic gameplay simulation, MSW Maker launch, world creation/save, and Play Preview execution are verified. Direct MCP injection is unavailable because MakerMCP returns an empty tool list, so the deliverable includes MSW-ready scripts, local harness checks, generated run evidence, and a created Maker world with at least the first project component resource visible in Workspace.
