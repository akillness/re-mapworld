"""Expanded MapleSurvivalExpedition simulation engine and balance loop.

Implements the design in docs/join_develop.md:
- 10-wave session with normal / elite / boss waves
- real damage exchange (monsters hit back), risk-gauge scaling
- consumables (potion, food) with drop tables
- escape decision at wave end ("extract now or one more wave?")
- monster collection (first-discovery passive bonuses)
- account meta settlement (score -> account exp)

The balance loop runs implement -> verify -> improve iterations against
machine-checkable acceptance criteria mirrored in seed.yaml.
"""
from __future__ import annotations

import copy
import json
import random
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BALANCE_PATH = ROOT / "balance_table.json"


def load_balance() -> dict:
    return json.loads(BALANCE_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- simulation


@dataclass
class Monster:
    name: str
    hp: float
    attack: float
    exp: int
    tier: str


@dataclass
class SessionResult:
    policy: str
    seed: int
    ok: bool = False
    outcome: str = "unknown"  # cleared | escaped | wiped | timeout
    seconds: int = 0
    final_wave: int = 0
    boss_defeated: bool = False
    deaths: int = 0
    score: int = 0
    level: int = 1
    kills: int = 0
    potions_used: int = 0
    food_used: int = 0
    min_health_ratio: float = 1.0
    collection: list[str] = field(default_factory=list)
    account_exp: int = 0
    damage_per_wave: dict[int, float] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)


class Session:
    """Deterministic single-session simulation at 1s ticks."""

    def __init__(self, balance: dict, policy: str, seed: int) -> None:
        self.b = balance
        self.policy = policy
        self.rng = random.Random(seed)
        self.result = SessionResult(policy=policy, seed=seed)

        p = balance["player"]
        self.max_health = p["max_health"]
        self.health = self.max_health
        self.max_hunger = p["max_hunger"]
        self.hunger = self.max_hunger
        self.level = 1
        self.exp = 0
        self.score = 0
        self.potions = balance["drops"]["starting_potions"]
        self.food = balance["drops"]["starting_food"]
        self.collection: list[str] = []
        self.alive: list[Monster] = []
        self.carry_damage = 0.0
        self.elite_spawned_this_wave = False

    # -- derived stats ----------------------------------------------------
    def attack_power(self) -> float:
        p = self.b["player"]
        bonus = 1.0 + len(self.collection) * self.b["collection"]["attack_bonus_per_entry"]
        return (p["base_attack"] + (self.level - 1) * p["attack_per_level"]) * bonus

    def effective_max_health(self) -> float:
        return self.max_health + len(self.collection) * self.b["collection"]["health_bonus_per_entry"]

    # -- mechanics ---------------------------------------------------------
    def spawn(self, wave_cfg: dict, risk: float) -> None:
        name = self.rng.choice(wave_cfg["pool"])
        spec = self.b["monsters"][name]
        hp_scale = 1.0 + risk * self.b["risk"]["hp_scale_at_full_risk"]
        self.alive.append(Monster(name, spec["hp"] * hp_scale, spec["attack"], spec["exp"], spec["tier"]))

    def spawn_named(self, name: str) -> None:
        spec = self.b["monsters"][name]
        self.alive.append(Monster(name, spec["hp"], spec["attack"], spec["exp"], spec["tier"]))

    def register_kill(self, mon: Monster, wave: int) -> None:
        self.result.kills += 1
        gained = mon.exp
        self.exp += gained
        self.score += gained
        if mon.name not in self.collection:
            self.collection.append(mon.name)
        d = self.b["drops"]
        if self.rng.random() < d["potion_chance"]:
            self.potions += 1
        if self.rng.random() < d["food_chance"]:
            self.food += 1
        p = self.b["player"]
        while self.exp >= self.level * p["exp_per_level_factor"]:
            self.exp -= self.level * p["exp_per_level_factor"]
            self.level += 1
            self.max_health += p["level_up_health_bonus"]
            self.health = self.effective_max_health()
            self.max_hunger += p["level_up_hunger_bonus"]
            self.hunger = self.max_hunger

    def consume(self) -> None:
        p = self.b["player"]
        threshold = p["potion_use_threshold"] if self.policy != "greedy" else 0.25
        if self.potions > 0 and self.health < self.effective_max_health() * threshold:
            self.potions -= 1
            self.health = min(self.effective_max_health(), self.health + p["potion_heal"])
            self.result.potions_used += 1
        if self.food > 0 and self.hunger < self.max_hunger * p["food_use_threshold"]:
            self.food -= 1
            self.hunger = min(self.max_hunger, self.hunger + p["food_restore"])
            self.result.food_used += 1

    def wants_escape(self, wave: int, target_wave: int) -> bool:
        ratio = self.health / self.effective_max_health()
        if self.policy == "greedy":
            return False
        if self.policy == "cautious":
            return wave >= 4 or ratio < 0.5
        # standard: full clear attempt, bail only when resources are gone
        return ratio < 0.2 and self.potions == 0

    # -- main loop ---------------------------------------------------------
    def run(self, max_seconds: int = 1200) -> SessionResult:
        s = self.b["session"]
        waves = {w["wave"]: w for w in self.b["waves"]}
        target_wave = s["target_wave"]
        wave = 1
        wave_cfg = waves[wave]
        wave_timer = s["base_wave_duration"] + wave * s["wave_duration_per_wave"]
        wave_duration = wave_timer
        spawn_timer = 0.0
        in_rest = False
        rest_timer = 0.0
        boss_spawned = False
        r = self.result

        for tick in range(1, max_seconds + 1):
            r.seconds = tick
            risk = 0.0 if in_rest else max(0.0, min(1.0, 1.0 - wave_timer / wave_duration))

            if not in_rest:
                # spawning
                spawn_timer += 1.0
                if wave_cfg["type"] == "boss" and not boss_spawned:
                    self.spawn_named(wave_cfg["boss"])
                    boss_spawned = True
                    r.events.append({"t": tick, "e": "boss_spawn", "wave": wave})
                if len(self.alive) < wave_cfg["max_alive"] and spawn_timer >= wave_cfg["spawn_interval"]:
                    spawn_timer = 0.0
                    self.spawn(wave_cfg, risk)
                    if (
                        wave_cfg["type"] == "elite"
                        and risk > 0.5
                        and not self.elite_spawned_this_wave
                    ):
                        self.spawn_named(wave_cfg["elite"])
                        self.elite_spawned_this_wave = True
                        r.events.append({"t": tick, "e": "elite_spawn", "wave": wave})

                # player attacks front monster
                dps = self.attack_power() + self.carry_damage
                self.carry_damage = 0.0
                while self.alive and dps > 0:
                    front = self.alive[0]
                    if dps >= front.hp:
                        dps -= front.hp
                        self.alive.pop(0)
                        self.register_kill(front, wave)
                    else:
                        front.hp -= dps
                        dps = 0.0
                # leftover dps beyond last kill is discarded (no carry across ticks with no target)

                # monsters attack back (engagement cap)
                cap = self.b["player"]["engagement_cap"]
                atk_scale = 1.0 + risk * self.b["risk"]["attack_scale_at_full_risk"]
                incoming = sum(m.attack for m in self.alive[:cap]) * atk_scale
                if incoming > 0:
                    self.health -= incoming
                    r.damage_per_wave[wave] = r.damage_per_wave.get(wave, 0.0) + incoming

            else:
                # campfire / safe-zone healing during rest phase (docs: 캠프/안전지대)
                heal = self.effective_max_health() * s.get("rest_heal_ratio", 0.0)
                self.health = min(self.effective_max_health(), self.health + heal)

            # hunger
            self.hunger = max(0.0, self.hunger - self.b["player"]["hunger_drain"])
            if self.hunger <= 0:
                self.health -= self.b["player"]["starvation_damage"]

            self.consume()
            r.min_health_ratio = min(r.min_health_ratio, max(0.0, self.health / self.effective_max_health()))

            if self.health <= 0:
                r.deaths += 1
                r.outcome = "wiped"
                break

            # wave progression
            if not in_rest:
                boss_alive = any(m.tier == "boss" for m in self.alive)
                wave_timer -= 1.0
                wave_over = (wave_timer <= 0 and not boss_alive) if wave_cfg["type"] == "boss" and boss_spawned else wave_timer <= 0
                if wave_cfg["type"] == "boss":
                    wave_over = boss_spawned and not boss_alive
                if wave_over:
                    if wave_cfg["type"] == "boss":
                        r.boss_defeated = True
                    r.events.append({"t": tick, "e": "wave_clear", "wave": wave})
                    if wave >= target_wave:
                        r.outcome = "cleared"
                        break
                    if self.wants_escape(wave, target_wave):
                        r.outcome = "escaped"
                        r.events.append({"t": tick, "e": "escape", "wave": wave})
                        break
                    in_rest = True
                    rest_timer = s["rest_duration"]
            else:
                rest_timer -= 1.0
                if rest_timer <= 0:
                    in_rest = False
                    wave += 1
                    wave_cfg = waves[wave]
                    wave_duration = s["base_wave_duration"] + wave * s["wave_duration_per_wave"]
                    wave_timer = wave_duration
                    spawn_timer = 0.0
                    self.alive.clear()
                    self.elite_spawned_this_wave = False
                    r.events.append({"t": tick, "e": "wave_start", "wave": wave})
        else:
            r.outcome = "timeout"

        r.final_wave = wave
        r.score = self.score
        r.level = self.level
        r.collection = list(self.collection)
        meta = self.b["meta"]
        keep = meta["escape_keep_ratio"] if r.outcome in ("cleared", "escaped") else meta["wipe_keep_ratio"]
        r.account_exp = int(self.score * keep * meta["account_exp_per_score"])
        r.ok = r.outcome in ("cleared", "escaped") and r.deaths == 0
        return r


def run_session(balance: dict, policy: str, seed: int) -> SessionResult:
    return Session(balance, policy, seed).run()


# ----------------------------------------------------------------- evaluate

SEEDS = [11, 23, 47]


def evaluate(balance: dict) -> dict:
    """Run all policies and check machine-checkable acceptance criteria."""
    s = balance["session"]
    runs = {p: [run_session(balance, p, seed) for seed in SEEDS] for p in ("standard", "cautious", "greedy")}
    std, cau, gre = runs["standard"], runs["cautious"], runs["greedy"]

    def all_(items, pred):
        return all(pred(r) for r in items)

    criteria = {}
    criteria["AC2_standard_full_clear"] = all_(
        std, lambda r: r.outcome == "cleared" and r.boss_defeated and r.deaths == 0
    )
    criteria["AC3_standard_session_length"] = all_(
        std, lambda r: s["min_session_seconds"] <= r.seconds <= s["max_session_seconds"]
    )
    criteria["AC4_cautious_safe_extract"] = all_(
        cau, lambda r: r.outcome == "escaped" and r.deaths == 0 and r.score > 0
    )
    criteria["AC5_greedy_risk_is_real"] = all_(gre, lambda r: r.min_health_ratio < 0.55) and all_(
        gre, lambda r: r.outcome in ("cleared", "wiped")
    )
    # difficulty monotonicity from standard runs: late waves hit harder
    mono_checks = []
    for r in std:
        dmg = r.damage_per_wave
        if len(dmg) >= 8:
            ws = sorted(dmg)
            increments = [dmg[ws[i + 1]] >= dmg[ws[i]] for i in range(len(ws) - 1)]
            mono_checks.append(dmg[ws[-1]] > dmg[ws[0]] and sum(increments) >= len(increments) * 0.6)
        else:
            mono_checks.append(False)
    criteria["AC6_difficulty_monotonic"] = all(mono_checks)
    criteria["AC7_collection_discovery"] = all_(std, lambda r: len(r.collection) >= 4)
    criteria["AC8_meta_settlement"] = all_(
        std + cau, lambda r: r.account_exp > 0
    )

    passed = sum(criteria.values())
    # soft objective for continued improvement once all hard criteria pass:
    # center standard session length in the target band, keep greedy danger
    # inside a meaningful band (0.05..0.45 min health ratio).
    mid = (s["min_session_seconds"] + s["max_session_seconds"]) / 2
    length_err = sum(abs(r.seconds - mid) / mid for r in std) / len(std)
    danger = sum(r.min_health_ratio for r in gre) / len(gre)
    danger_err = abs(danger - 0.25)
    soft = max(0.0, 1.0 - (length_err * 0.5 + danger_err))

    return {
        "criteria": criteria,
        "passed": passed,
        "total": len(criteria),
        "all_passed": passed == len(criteria),
        "soft_score": round(soft, 4),
        "fitness": round(passed + soft, 4),
        "observed": {
            "standard_seconds": [r.seconds for r in std],
            "standard_outcomes": [r.outcome for r in std],
            "standard_levels": [r.level for r in std],
            "standard_collection": [len(r.collection) for r in std],
            "cautious_outcomes": [r.outcome for r in cau],
            "greedy_min_health": [round(r.min_health_ratio, 3) for r in gre],
            "greedy_outcomes": [r.outcome for r in gre],
        },
        "runs": runs,
    }


# ------------------------------------------------------------- balance loop

# tunable knobs: (json path, min, max, relative step)
KNOBS = [
    (("session", "base_wave_duration"), 20.0, 60.0, 0.12),
    (("session", "rest_heal_ratio"), 0.0, 0.15, 0.25),
    (("session", "wave_duration_per_wave"), 1.0, 10.0, 0.2),
    (("player", "base_attack"), 4.0, 30.0, 0.12),
    (("player", "attack_per_level"), 0.5, 6.0, 0.2),
    (("player", "potion_heal"), 20.0, 90.0, 0.15),
    (("player", "max_health"), 80.0, 220.0, 0.1),
    (("drops", "potion_chance"), 0.05, 0.5, 0.2),
    (("drops", "food_chance"), 0.05, 0.5, 0.2),
    (("risk", "attack_scale_at_full_risk"), 0.1, 1.5, 0.2),
    (("monsters", "BossBalrog", "hp"), 600.0, 4000.0, 0.15),
    (("monsters", "BossBalrog", "attack"), 6.0, 40.0, 0.15),
    (("monsters", "EliteGolem", "attack"), 4.0, 25.0, 0.15),
]


def get_path(d: dict, path: tuple) -> float:
    for key in path:
        d = d[key]
    return d


def set_path(d: dict, path: tuple, value: float) -> None:
    for key in path[:-1]:
        d = d[key]
    d[path[-1]] = round(value, 4)


def diagnose_and_adjust(balance: dict, ev: dict, rng: random.Random) -> tuple[dict, str]:
    """Targeted improvement: read failing criteria and nudge the right knobs."""
    b = copy.deepcopy(balance)
    c = ev["criteria"]
    obs = ev["observed"]
    s = b["session"]
    actions: list[str] = []

    def bump(path: tuple, factor: float, reason: str) -> None:
        for knob_path, lo, hi, _ in KNOBS:
            if knob_path == path:
                cur = get_path(b, path)
                set_path(b, path, max(lo, min(hi, cur * factor)))
                actions.append(f"{'.'.join(map(str, path))}*{factor:.2f} ({reason})")
                return

    if not c["AC2_standard_full_clear"]:
        if "wiped" in obs["standard_outcomes"]:
            bump(("player", "base_attack"), 1.1, "standard wiped: kill faster")
            bump(("player", "attack_per_level"), 1.08, "standard wiped: kill faster")
            bump(("player", "potion_heal"), 1.1, "standard wiped")
            bump(("drops", "potion_chance"), 1.12, "standard wiped")
            bump(("session", "rest_heal_ratio"), 1.2, "standard wiped")
            bump(("monsters", "EliteGolem", "attack"), 0.92, "standard wiped")
            bump(("monsters", "BossBalrog", "attack"), 0.92, "standard wiped")
        else:  # timeout: not enough damage
            bump(("player", "base_attack"), 1.12, "standard timeout")
            bump(("monsters", "BossBalrog", "hp"), 0.9, "standard timeout")
    if not c["AC3_standard_session_length"]:
        mean_secs = sum(obs["standard_seconds"]) / len(obs["standard_seconds"])
        if mean_secs > s["max_session_seconds"]:
            bump(("session", "base_wave_duration"), 0.9, "session too long")
            bump(("player", "base_attack"), 1.08, "session too long")
        else:
            bump(("session", "base_wave_duration"), 1.1, "session too short")
            bump(("session", "wave_duration_per_wave"), 1.1, "session too short")
    if not c["AC5_greedy_risk_is_real"]:
        if all(x >= 0.55 for x in obs["greedy_min_health"]):
            bump(("risk", "attack_scale_at_full_risk"), 1.15, "greedy too safe")
            bump(("monsters", "BossBalrog", "attack"), 1.1, "greedy too safe")
        if "wiped" not in obs["greedy_outcomes"] and "cleared" not in obs["greedy_outcomes"]:
            bump(("player", "base_attack"), 1.08, "greedy stalls")
    if not c["AC6_difficulty_monotonic"]:
        bump(("risk", "attack_scale_at_full_risk"), 1.08, "flat difficulty")
        bump(("monsters", "EliteGolem", "attack"), 1.06, "flat difficulty")
    if not c["AC7_collection_discovery"]:
        bump(("session", "wave_duration_per_wave"), 1.05, "low discovery")

    if not actions:
        # all hard criteria pass: random-neighborhood refinement of one knob
        path, lo, hi, step = rng.choice(KNOBS)
        cur = get_path(b, path)
        factor = 1.0 + rng.uniform(-step, step)
        set_path(b, path, max(lo, min(hi, cur * factor)))
        actions.append(f"{'.'.join(map(str, path))}*{factor:.3f} (refine)")
    return b, "; ".join(actions)


def random_kick(balance: dict, rng: random.Random, magnitude: float) -> tuple[dict, str]:
    """Escape a plateau: jump 2-3 random knobs to random values in their bounds."""
    b = copy.deepcopy(balance)
    picked = rng.sample(KNOBS, k=min(len(KNOBS), 2 + int(magnitude)))
    names = []
    for path, lo, hi, _ in picked:
        cur = get_path(b, path)
        span = (hi - lo) * min(1.0, 0.25 * magnitude)
        value = max(lo, min(hi, cur + rng.uniform(-span, span)))
        set_path(b, path, value)
        names.append(f"{'.'.join(map(str, path))}={round(value, 3)}")
    return b, f"kick[{magnitude:.0f}]: " + ", ".join(names)


def balance_loop(iterations: int = 60, rng_seed: int = 7) -> dict:
    rng = random.Random(rng_seed)
    current = load_balance()
    ev = evaluate(current)
    best = copy.deepcopy(current)
    best_passed = ev["passed"]
    best_fitness = ev["fitness"]
    stuck = 0
    log: list[dict] = [{
        "iteration": 0,
        "phase": "baseline",
        "passed": ev["passed"],
        "total": ev["total"],
        "fitness": ev["fitness"],
        "criteria": ev["criteria"],
        "observed": ev["observed"],
        "action": "initial evaluation",
        "accepted": True,
    }]

    for i in range(1, iterations + 1):
        if stuck >= 5:
            candidate, action = random_kick(best, rng, magnitude=1 + (stuck - 5) // 3)
            phase = "kick"
        else:
            candidate, action = diagnose_and_adjust(best, evaluate(best), rng)
            phase = "improve" if "refine" not in action else "refine"
        cev = evaluate(candidate)
        # criteria-count-first acceptance: more hard criteria always wins;
        # on ties, fitness (criteria + soft objective) must not regress.
        accepted = cev["passed"] > best_passed or (
            cev["passed"] == best_passed and cev["fitness"] >= best_fitness
        )
        if accepted:
            improved = cev["passed"] > best_passed or cev["fitness"] > best_fitness
            best = candidate
            best_passed = cev["passed"]
            best_fitness = cev["fitness"]
            stuck = 0 if improved else stuck + 1
        else:
            stuck += 1
        log.append({
            "iteration": i,
            "phase": phase,
            "passed": cev["passed"],
            "total": cev["total"],
            "fitness": cev["fitness"],
            "criteria": cev["criteria"],
            "observed": cev["observed"],
            "action": action,
            "accepted": accepted,
        })

    final_ev = evaluate(best)
    BALANCE_PATH.write_text(json.dumps(best, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "iterations": iterations,
        "final_fitness": final_ev["fitness"],
        "final_passed": final_ev["passed"],
        "final_total": final_ev["total"],
        "all_passed": final_ev["all_passed"],
        "final_criteria": final_ev["criteria"],
        "final_observed": final_ev["observed"],
        "log": log,
    }
