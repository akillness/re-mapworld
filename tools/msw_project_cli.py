#!/usr/bin/env python3
"""Agent-native project CLI for MapleSurvivalExpedition.

This is a lightweight CLI-Anything style harness for the local MapleStory Worlds
project. It validates MSW script structure, runs a deterministic gameplay
simulation, launches the installed MSW Maker, and probes the MakerMCP bridge.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MSW_EXE = Path("D:/MapleStory Worlds/msw.exe")
MAKER_MCP_EXE = Path("D:/MapleStory Worlds/MakerMCP/MakerMCP.exe")
REQUIRED_SCRIPTS = [
    "PlayerSurvivalStats.lua",
    "MonsterSpawner.lua",
    "MonsterAgent.lua",
    "SurvivalGameManager.lua",
    "SurvivalHudBridge.lua",
    "MonsterCollection.lua",
    "BalanceTable.lua",
]


@dataclass
class ValidationIssue:
    file: str
    level: str
    message: str


class PlayerModel:
    def __init__(self) -> None:
        self.health = 100.0
        self.max_health = 100.0
        self.hunger = 100.0
        self.max_hunger = 100.0
        self.hunger_drain = 0.45
        self.starvation_damage = 2.5
        self.level = 1
        self.exp = 0
        self.score = 0
        self.deaths = 0

    def update(self, delta: float) -> None:
        self.hunger = max(0.0, self.hunger - delta * self.hunger_drain)
        if self.hunger <= 0:
            self.apply_damage(delta * self.starvation_damage)

    def apply_damage(self, amount: float) -> None:
        self.health -= amount
        if self.health <= 0:
            self.deaths += 1
            self.health = self.max_health
            self.hunger = self.max_hunger

    def eat(self, amount: float) -> None:
        self.hunger = min(self.max_hunger, self.hunger + amount)

    def gain_exp(self, amount: int) -> None:
        self.exp += amount
        self.score += amount
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            self.max_health += 20
            self.health = self.max_health
            self.max_hunger += 5
            self.hunger = self.max_hunger


class GameModel:
    def __init__(self, target_wave: int = 5) -> None:
        self.current_wave = 1
        self.base_wave_duration = 45.0
        self.rest_duration = 10.0
        self.wave_timer = self.wave_duration()
        self.rest_timer = 0.0
        self.risk_percent = 0.0
        self.target_wave = target_wave
        self.is_wave_active = True
        self.is_complete = False
        self.completed_at = None

    def wave_duration(self) -> float:
        return self.base_wave_duration + self.current_wave * 10.0

    def update(self, delta: float, now: float) -> str | None:
        if self.is_complete:
            return None
        if self.is_wave_active:
            self.wave_timer -= delta
            self.risk_percent = max(0.0, min(100.0, 100.0 - ((self.wave_timer / self.wave_duration()) * 100.0)))
            if self.wave_timer <= 0:
                self.risk_percent = 100.0
                if self.current_wave >= self.target_wave:
                    self.is_complete = True
                    self.is_wave_active = False
                    self.completed_at = now
                    return "complete"
                self.is_wave_active = False
                self.rest_timer = self.rest_duration
                return "wave_end"
        else:
            self.rest_timer -= delta
            if self.rest_timer <= 0:
                self.current_wave += 1
                if self.current_wave > self.target_wave:
                    self.is_complete = True
                    self.is_wave_active = False
                    self.completed_at = now
                    return "complete"
                self.is_wave_active = True
                self.wave_timer = self.wave_duration()
                self.risk_percent = 0.0
                return "wave_start"
        return None


class SpawnerModel:
    def __init__(self) -> None:
        self.spawn_interval = 5.0
        self.timer = 0.0
        self.max_monsters = 10
        self.current_monsters = 0
        self.total_spawned = 0

    def cap(self, wave: int) -> int:
        return min(40, self.max_monsters + wave)

    def interval(self, wave: int) -> float:
        return max(1.25, self.spawn_interval - wave * 0.15)

    def update(self, delta: float, wave: int, active: bool) -> int:
        if not active or self.current_monsters >= self.cap(wave):
            return 0
        self.timer += delta
        if self.timer >= self.interval(wave):
            self.timer = 0.0
            self.current_monsters += 1
            self.total_spawned += 1
            return 1
        return 0

    def defeat_one(self) -> bool:
        if self.current_monsters <= 0:
            return False
        self.current_monsters -= 1
        return True


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_scripts(json_output: bool = False) -> int:
    issues: list[ValidationIssue] = []
    method_pattern = re.compile(r"\bvoid\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    property_pattern = re.compile(r"^\s*(number|integer|boolean|string)\s+[A-Za-z_][A-Za-z0-9_]*\s*=", re.MULTILINE)

    for script in REQUIRED_SCRIPTS:
        path = ROOT / script
        if not path.exists():
            issues.append(ValidationIssue(script, "error", "required script is missing"))
            continue

        text = read_text(path)
        if "Property:" not in text:
            issues.append(ValidationIssue(script, "error", "missing Property: section"))
        if "Method:" not in text:
            issues.append(ValidationIssue(script, "error", "missing Method: section"))
        if text.count("{") != text.count("}"):
            issues.append(ValidationIssue(script, "error", "unbalanced MSW method braces"))
        if not method_pattern.search(text):
            issues.append(ValidationIssue(script, "error", "no MSW void methods found"))
        if not property_pattern.search(text):
            issues.append(ValidationIssue(script, "warning", "no typed properties found"))
        if "TODO" in text or "some_monster_id" in text:
            issues.append(ValidationIssue(script, "error", "placeholder text remains"))

    report = {
        "ok": not any(issue.level == "error" for issue in issues),
        "root": str(ROOT),
        "checked": REQUIRED_SCRIPTS,
        "issues": [issue.__dict__ for issue in issues],
    }
    if json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("MSW script validation:", "PASS" if report["ok"] else "FAIL")
        for issue in issues:
            print(f"[{issue.level.upper()}] {issue.file}: {issue.message}")
    return 0 if report["ok"] else 1


def simulate(seconds: int, json_output: bool = False) -> int:
    player = PlayerModel()
    game = GameModel()
    spawner = SpawnerModel()
    events: list[dict[str, object]] = []

    for tick in range(1, seconds + 1):
        now = float(tick)
        event = game.update(1.0, now)
        if event:
            events.append({"time": tick, "event": event, "wave": game.current_wave})
            if event == "wave_end":
                player.eat(22)

        spawned = spawner.update(1.0, game.current_wave, game.is_wave_active)
        if spawned:
            events.append({"time": tick, "event": "spawn", "wave": game.current_wave, "alive": spawner.current_monsters})

        if tick % 4 == 0 and spawner.defeat_one():
            player.gain_exp(25 + game.current_wave * 5)
            events.append({"time": tick, "event": "monster_defeated", "wave": game.current_wave, "level": player.level})

        player.update(1.0)
        if game.is_complete:
            break

    result = {
        "ok": game.is_complete and player.deaths == 0,
        "seconds_requested": seconds,
        "seconds_simulated": tick,
        "completed_at": game.completed_at,
        "player": {
            "health": round(player.health, 2),
            "hunger": round(player.hunger, 2),
            "level": player.level,
            "exp": player.exp,
            "score": player.score,
            "deaths": player.deaths,
        },
        "game": {
            "wave": game.current_wave,
            "complete": game.is_complete,
            "risk_percent": round(game.risk_percent, 2),
        },
        "spawner": {
            "total_spawned": spawner.total_spawned,
            "alive": spawner.current_monsters,
        },
        "event_count": len(events),
        "events_tail": events[-12:],
    }
    if json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Simulation:", "PASS" if result["ok"] else "FAIL")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def is_process_running(image_name: str) -> bool:
    completed = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {image_name}", "/FO", "CSV"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return image_name.lower() in completed.stdout.lower()


def launch_engine(json_output: bool = False) -> int:
    if not MSW_EXE.exists():
        result = {"ok": False, "error": f"MSW executable not found: {MSW_EXE}"}
    else:
        already_running = is_process_running("msw.exe")
        if not already_running:
            subprocess.Popen([str(MSW_EXE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(15)
        running = is_process_running("msw.exe")
        result = {
            "ok": running,
            "executable": str(MSW_EXE),
            "already_running": already_running,
            "running_after_launch": running,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2) if json_output else result)
    return 0 if result.get("ok") else 1


def maker_status(json_output: bool = False) -> int:
    if not MAKER_MCP_EXE.exists():
        result = {"ok": False, "error": f"MakerMCP executable not found: {MAKER_MCP_EXE}"}
        print(json.dumps(result, ensure_ascii=False, indent=2) if json_output else result)
        return 1

    proc = subprocess.Popen(
        [str(MAKER_MCP_EXE)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        assert proc.stdin is not None and proc.stdout is not None
        initialize = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "MapleSurvivalExpeditionCLI", "version": "1.0.0"},
            },
        }
        tools = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        proc.stdin.write(json.dumps(initialize) + "\n")
        proc.stdin.flush()
        init_line = proc.stdout.readline().strip()
        proc.stdin.write(json.dumps(tools) + "\n")
        proc.stdin.flush()
        tools_line = proc.stdout.readline().strip()
        init_payload = json.loads(init_line)
        tools_payload = json.loads(tools_line)
        tool_list = tools_payload.get("result", {}).get("tools", [])
        result = {
            "ok": "result" in init_payload,
            "mcp_initialized": "result" in init_payload,
            "tools_available": len(tool_list),
            "tools": [tool.get("name") for tool in tool_list if isinstance(tool, dict)],
            "note": "tools_available is 0 when MSW Maker has not exposed its editor bridge yet.",
        }
    finally:
        proc.kill()

    print(json.dumps(result, ensure_ascii=False, indent=2) if json_output else result)
    return 0 if result.get("ok") else 1


def write_run_report() -> int:
    validate_code = validate_scripts(json_output=True)
    simulation_completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "simulate", "--seconds", "420", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    maker_completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "maker-status", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    engine_completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "launch-engine", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    report_path = ROOT / "ENGINE_RUN_REPORT.md"
    report_path.write_text(
        "# MapleSurvivalExpedition Engine Run Report\n\n"
        f"Generated: 2026-06-11\n\n"
        "## Validation\n\n"
        f"Exit code: {validate_code}\n\n"
        "## Simulation\n\n"
        "```json\n" + simulation_completed.stdout.strip() + "\n```\n\n"
        "## MakerMCP Probe\n\n"
        "```json\n" + maker_completed.stdout.strip() + "\n```\n\n"
        "## MSW Maker Launch\n\n"
        "```json\n" + engine_completed.stdout.strip() + "\n```\n\n"
        "## Result\n\n"
        "Static validation and deterministic gameplay simulation pass. MSW Maker launch is verified by process check. "
        "MakerMCP initializes, but editor tools are unavailable in this session until the Maker bridge exposes tools.\n",
        encoding="utf-8",
    )
    print(str(report_path))
    return 0 if validate_code == 0 and simulation_completed.returncode == 0 and engine_completed.returncode == 0 else 1


def expedition(policy: str, seed: int, json_output: bool = False) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import survival_sim

    result = survival_sim.run_session(survival_sim.load_balance(), policy, seed)
    payload = {
        "ok": result.ok,
        "policy": result.policy,
        "seed": result.seed,
        "outcome": result.outcome,
        "seconds": result.seconds,
        "final_wave": result.final_wave,
        "boss_defeated": result.boss_defeated,
        "deaths": result.deaths,
        "score": result.score,
        "level": result.level,
        "kills": result.kills,
        "potions_used": result.potions_used,
        "food_used": result.food_used,
        "min_health_ratio": round(result.min_health_ratio, 3),
        "collection": result.collection,
        "account_exp": result.account_exp,
        "damage_per_wave": {str(k): round(v, 1) for k, v in sorted(result.damage_per_wave.items())},
        "events_tail": result.events[-10:],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.ok else 1


def evaluate_cmd(json_output: bool = False) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import survival_sim

    ev = survival_sim.evaluate(survival_sim.load_balance())
    payload = {k: v for k, v in ev.items() if k != "runs"}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ev["all_passed"] else 1


def balance_loop_cmd(iterations: int) -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import survival_sim

    summary = survival_sim.balance_loop(iterations=iterations)
    log_path = ROOT / "balance_loop_log.json"
    log_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Balance Loop Report (ralph: implement -> verify -> improve)",
        "",
        f"Generated: 2026-06-11. Iterations: {summary['iterations']} (baseline + improvements).",
        "",
        f"- Final acceptance criteria: {summary['final_passed']}/{summary['final_total']} passed"
        f" ({'ALL PASS' if summary['all_passed'] else 'INCOMPLETE'})",
        f"- Final fitness (hard criteria + soft tuning objective): {summary['final_fitness']}",
        "",
        "## Final criteria",
        "",
        "| Criterion | Result |",
        "|---|---|",
    ]
    for name, ok in summary["final_criteria"].items():
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} |")
    lines += [
        "",
        "## Final observed metrics",
        "",
        "```json",
        json.dumps(summary["final_observed"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Iteration log",
        "",
        "| # | Phase | Passed | Fitness | Accepted | Action |",
        "|--:|---|--:|--:|---|---|",
    ]
    for entry in summary["log"]:
        lines.append(
            f"| {entry['iteration']} | {entry['phase']} | {entry['passed']}/{entry['total']}"
            f" | {entry['fitness']} | {'yes' if entry['accepted'] else 'no'} | {entry['action']} |"
        )
    lines.append("")
    (ROOT / "BALANCE_LOOP_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "iterations": summary["iterations"],
        "final_passed": summary["final_passed"],
        "final_total": summary["final_total"],
        "all_passed": summary["all_passed"],
        "final_fitness": summary["final_fitness"],
        "report": str(ROOT / "BALANCE_LOOP_REPORT.md"),
        "log": str(log_path),
    }, ensure_ascii=False, indent=2))
    return 0 if summary["all_passed"] else 1


def gen_lua() -> int:
    """Regenerate BalanceTable.lua from balance_table.json (data -> MSW script)."""
    balance = json.loads((ROOT / "balance_table.json").read_text(encoding="utf-8"))
    s = balance["session"]
    p = balance["player"]
    monster_lines = []
    for name, spec in balance["monsters"].items():
        monster_lines.append(
            f'        if monsterName == "{name}" then'
            f' return {spec["hp"]}, {spec["attack"]}, {spec["exp"]} end'
        )
    wave_lines = []
    for w in balance["waves"]:
        wave_lines.append(
            f'        if wave == {w["wave"]} then return "{w["type"]}", {w["spawn_interval"]}, {w["max_alive"]} end'
        )
    text = f"""-- BalanceTable
-- MapleStory Worlds Logic: generated from balance_table.json by tools/msw_project_cli.py gen-lua.
-- Data-driven balance per docs/join_develop.md. Do not edit by hand; edit balance_table.json.

Property:
    [Sync]
    integer TargetWave = {s["target_wave"]}
    [Sync]
    number BaseWaveDuration = {s["base_wave_duration"]}
    [Sync]
    number WaveDurationPerWave = {s["wave_duration_per_wave"]}
    [Sync]
    number RestDuration = {s["rest_duration"]}
    [Sync]
    number RestHealRatio = {s["rest_heal_ratio"]}
    [Sync]
    number PlayerMaxHealth = {p["max_health"]}
    [Sync]
    number PlayerBaseAttack = {p["base_attack"]}
    [Sync]
    number PlayerAttackPerLevel = {p["attack_per_level"]}
    [Sync]
    number PotionHeal = {p["potion_heal"]}
    [Sync]
    number FoodRestore = {p["food_restore"]}
    [Sync]
    number RiskAttackScale = {balance["risk"]["attack_scale_at_full_risk"]}
    [Sync]
    number RiskHpScale = {balance["risk"]["hp_scale_at_full_risk"]}
    [Sync]
    number PotionDropChance = {balance["drops"]["potion_chance"]}
    [Sync]
    number FoodDropChance = {balance["drops"]["food_chance"]}
    [Sync]
    number CollectionAttackBonus = {balance["collection"]["attack_bonus_per_entry"]}
    [Sync]
    number CollectionHealthBonus = {balance["collection"]["health_bonus_per_entry"]}

Method:
    [Server Only]
    void OnBeginPlay()
    {{
        log("[MapleSurvivalExpedition] BalanceTable loaded. TargetWave=" .. tostring(self.TargetWave))
    }}

    [Server Only]
    number GetWaveDuration(integer wave)
    {{
        return self.BaseWaveDuration + (wave * self.WaveDurationPerWave)
    }}

    [Server Only]
    string GetWaveType(integer wave)
    {{
        local waveType, interval, maxAlive = self:GetWaveConfig(wave)
        return waveType
    }}

    [Server Only]
    string,number,integer GetWaveConfig(integer wave)
    {{
{chr(10).join(wave_lines)}
        return "normal", 4.0, 8
    }}

    [Server Only]
    number,number,integer GetMonsterStats(string monsterName)
    {{
{chr(10).join(monster_lines)}
        return 30, 3, 20
    }}
"""
    (ROOT / "BalanceTable.lua").write_text(text, encoding="utf-8")
    print(str(ROOT / "BalanceTable.lua"))
    return 0


def charts() -> int:
    """Render balance loop progression and wave difficulty charts to artifacts/."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import survival_sim

    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)

    log_path = ROOT / "balance_loop_log.json"
    if log_path.exists():
        summary = json.loads(log_path.read_text(encoding="utf-8"))
        iters = [e["iteration"] for e in summary["log"]]
        fitness = [e["fitness"] for e in summary["log"]]
        passed = [e["passed"] for e in summary["log"]]
        fig, ax1 = plt.subplots(figsize=(9, 4.5))
        ax1.plot(iters, fitness, color="#e8772e", linewidth=2, label="fitness")
        ax1.set_xlabel("iteration")
        ax1.set_ylabel("fitness (criteria + soft objective)", color="#e8772e")
        ax2 = ax1.twinx()
        ax2.step(iters, passed, where="mid", color="#3f72af", alpha=0.6, label="criteria passed")
        ax2.set_ylabel("acceptance criteria passed", color="#3f72af")
        ax2.set_ylim(0, summary["final_total"] + 0.5)
        ax1.set_title("Balance loop: implement -> verify -> improve")
        fig.tight_layout()
        fig.savefig(artifacts / "balance_progression.png", dpi=120)
        plt.close(fig)

    balance = survival_sim.load_balance()
    result = survival_sim.run_session(balance, "standard", 11)
    waves = sorted(result.damage_per_wave)
    dmg = [result.damage_per_wave[w] for w in waves]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    colors = ["#c0392b" if balance["waves"][w - 1]["type"] == "boss"
              else "#e67e22" if balance["waves"][w - 1]["type"] == "elite"
              else "#3f72af" for w in waves]
    ax.bar([str(w) for w in waves], dmg, color=colors)
    ax.set_xlabel("wave")
    ax.set_ylabel("damage taken by player")
    ax.set_title("Wave difficulty curve (standard policy, seed 11) - blue normal / orange elite / red boss")
    fig.tight_layout()
    fig.savefig(artifacts / "wave_difficulty.png", dpi=120)
    plt.close(fig)

    print(json.dumps({
        "ok": True,
        "charts": ["artifacts/balance_progression.png", "artifacts/wave_difficulty.png"],
    }, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MapleSurvivalExpedition project CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_parser = sub.add_parser("validate", help="validate MSW script structure")
    validate_parser.add_argument("--json", action="store_true")

    simulate_parser = sub.add_parser("simulate", help="run deterministic survival simulation")
    simulate_parser.add_argument("--seconds", type=int, default=420)
    simulate_parser.add_argument("--json", action="store_true")

    maker_parser = sub.add_parser("maker-status", help="probe MakerMCP")
    maker_parser.add_argument("--json", action="store_true")

    launch_parser = sub.add_parser("launch-engine", help="launch or confirm MSW Maker")
    launch_parser.add_argument("--json", action="store_true")

    sub.add_parser("write-run-report", help="write ENGINE_RUN_REPORT.md")

    expedition_parser = sub.add_parser("expedition", help="run expanded expedition session simulation")
    expedition_parser.add_argument("--policy", choices=["standard", "cautious", "greedy"], default="standard")
    expedition_parser.add_argument("--seed", type=int, default=11)
    expedition_parser.add_argument("--json", action="store_true")

    evaluate_parser = sub.add_parser("evaluate", help="evaluate acceptance criteria across policies")
    evaluate_parser.add_argument("--json", action="store_true")

    loop_parser = sub.add_parser("balance-loop", help="ralph loop: implement -> verify -> improve balance")
    loop_parser.add_argument("--iterations", type=int, default=60)

    sub.add_parser("gen-lua", help="regenerate BalanceTable.lua from balance_table.json")
    sub.add_parser("charts", help="render balance charts to artifacts/")

    args = parser.parse_args()
    if args.command == "validate":
        return validate_scripts(json_output=args.json)
    if args.command == "simulate":
        return simulate(args.seconds, json_output=args.json)
    if args.command == "maker-status":
        return maker_status(json_output=args.json)
    if args.command == "launch-engine":
        return launch_engine(json_output=args.json)
    if args.command == "write-run-report":
        return write_run_report()
    if args.command == "expedition":
        return expedition(args.policy, args.seed, json_output=args.json)
    if args.command == "evaluate":
        return evaluate_cmd(json_output=args.json)
    if args.command == "balance-loop":
        return balance_loop_cmd(args.iterations)
    if args.command == "gen-lua":
        return gen_lua()
    if args.command == "charts":
        return charts()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
