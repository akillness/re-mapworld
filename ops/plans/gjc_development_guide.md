# gjc Development Guide (Generated from engine_trace.log)

## 1. Current Status Analysis
- **Last Trace**: [Thu Jun 11 07:41:32 KST 2026]
- **Status**: [REPORT] Waiting for Nexon Login.
- **Gap Identification**: The engine is stuck at the authentication layer. Scripts cannot be hot-swapped until the editor environment is fully loaded.

## 2. Implementation Directives for gjc
- **Priority 1 (Authentication Bypass/Handling)**: Focus on detecting the transition from 'Login' to 'World Editor'.
- **Priority 2 (Hot-swap Readiness)**: Ensure the /tmp/MapleSurvivalExpedition/scripts/ directory is synced as soon as the process 'mapleworld' enters the 'Editing' state.
- **Priority 3 (UI Sync)**: Implement visual verification for the 'Danger Gauge' (1% / 10s increment) once the play-test mode is active.

## 3. Screen Analysis Tasks
- Monitor for the appearance of the "World Create/Edit" button after login.
- Identify the coordinates of the "Play" button to trigger the ooo_run_strategy.

## 4. Maintenance
- This guide must be updated every time logs/engine_trace.log reports a state change.
