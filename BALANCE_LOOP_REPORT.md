# Balance Loop Report (ralph: implement -> verify -> improve)

Generated: 2026-06-11. Iterations: 80 (baseline + improvements).

- Final acceptance criteria: 7/7 passed (ALL PASS)
- Final fitness (hard criteria + soft tuning objective): 7.9534

## Final criteria

| Criterion | Result |
|---|---|
| AC2_standard_full_clear | PASS |
| AC3_standard_session_length | PASS |
| AC4_cautious_safe_extract | PASS |
| AC5_greedy_risk_is_real | PASS |
| AC6_difficulty_monotonic | PASS |
| AC7_collection_discovery | PASS |
| AC8_meta_settlement | PASS |

## Final observed metrics

```json
{
  "standard_seconds": [
    556,
    556,
    556
  ],
  "standard_outcomes": [
    "cleared",
    "cleared",
    "cleared"
  ],
  "standard_levels": [
    11,
    11,
    11
  ],
  "standard_collection": [
    7,
    7,
    7
  ],
  "cautious_outcomes": [
    "escaped",
    "escaped",
    "escaped"
  ],
  "greedy_min_health": [
    0.251,
    0.251,
    0.251
  ],
  "greedy_outcomes": [
    "cleared",
    "cleared",
    "cleared"
  ]
}
```

## Iteration log

| # | Phase | Passed | Fitness | Accepted | Action |
|--:|---|--:|--:|---|---|
| 0 | baseline | 5/7 | 5.6748 | yes | initial evaluation |
| 1 | improve | 4/7 | 4.7421 | no | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 2 | improve | 4/7 | 4.7421 | no | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 3 | improve | 4/7 | 4.7421 | no | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 4 | improve | 4/7 | 4.7421 | no | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 5 | improve | 4/7 | 4.7421 | no | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 6 | kick | 5/7 | 5.6882 | yes | kick[1]: player.potion_heal=77.756, session.wave_duration_per_wave=4.239, player.max_health=122.512 |
| 7 | improve | 5/7 | 5.7902 | yes | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 8 | improve | 6/7 | 6.8028 | yes | player.base_attack*1.10 (standard wiped: kill faster); player.attack_per_level*1.08 (standard wiped: kill faster); player.potion_heal*1.10 (standard wiped); drops.potion_chance*1.12 (standard wiped); session.rest_heal_ratio*1.20 (standard wiped); monsters.EliteGolem.attack*0.92 (standard wiped); monsters.BossBalrog.attack*0.92 (standard wiped); risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 9 | improve | 6/7 | 6.8041 | yes | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 10 | improve | 6/7 | 6.8036 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 11 | improve | 6/7 | 6.8036 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 12 | improve | 6/7 | 6.8036 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 13 | improve | 6/7 | 6.8036 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 14 | improve | 6/7 | 6.8036 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 15 | kick | 5/7 | 5.8855 | no | kick[1]: player.potion_heal=90.0, risk.attack_scale_at_full_risk=0.726, session.base_wave_duration=36.973 |
| 16 | kick | 6/7 | 6.8059 | yes | kick[1]: player.max_health=93.862, session.rest_heal_ratio=0.066, player.base_attack=15.139 |
| 17 | improve | 6/7 | 6.8066 | yes | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 18 | improve | 6/7 | 6.8042 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 19 | improve | 6/7 | 6.8042 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 20 | improve | 6/7 | 6.8042 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 21 | improve | 6/7 | 6.8042 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 22 | improve | 6/7 | 6.8042 | no | risk.attack_scale_at_full_risk*1.08 (flat difficulty); monsters.EliteGolem.attack*1.06 (flat difficulty) |
| 23 | kick | 7/7 | 7.8084 | yes | kick[1]: session.rest_heal_ratio=0.076, player.base_attack=20.959, monsters.BossBalrog.hp=1631.075 |
| 24 | refine | 7/7 | 7.8068 | no | player.max_health*0.910 (refine) |
| 25 | refine | 6/7 | 6.8065 | no | player.base_attack*0.891 (refine) |
| 26 | refine | 7/7 | 7.8159 | yes | session.wave_duration_per_wave*0.916 (refine) |
| 27 | refine | 7/7 | 7.8173 | yes | session.wave_duration_per_wave*1.016 (refine) |
| 28 | refine | 7/7 | 7.821 | yes | risk.attack_scale_at_full_risk*0.923 (refine) |
| 29 | refine | 7/7 | 7.824 | yes | monsters.BossBalrog.hp*0.904 (refine) |
| 30 | refine | 7/7 | 7.8196 | no | risk.attack_scale_at_full_risk*1.028 (refine) |
| 31 | refine | 6/7 | 6.8204 | no | player.base_attack*0.969 (refine) |
| 32 | refine | 7/7 | 7.824 | yes | drops.food_chance*1.085 (refine) |
| 33 | refine | 7/7 | 7.8216 | no | risk.attack_scale_at_full_risk*0.824 (refine) |
| 34 | refine | 7/7 | 7.824 | yes | player.base_attack*0.999 (refine) |
| 35 | kick | 7/7 | 7.8223 | no | kick[1]: drops.food_chance=0.318, player.max_health=123.502, player.potion_heal=85.155 |
| 36 | kick | 6/7 | 6.8537 | no | kick[1]: player.base_attack=15.505, session.wave_duration_per_wave=3.047, monsters.EliteGolem.attack=9.374 |
| 37 | kick | 7/7 | 7.8201 | no | kick[1]: player.potion_heal=82.578, monsters.BossBalrog.attack=17.089, drops.potion_chance=0.4 |
| 38 | kick | 6/7 | 6.8549 | no | kick[2]: player.max_health=154.519, session.wave_duration_per_wave=3.241, player.potion_heal=90.0, monsters.BossBalrog.attack=6.0 |
| 39 | kick | 7/7 | 7.8263 | yes | kick[2]: drops.food_chance=0.413, risk.attack_scale_at_full_risk=1.055, player.potion_heal=90.0, monsters.BossBalrog.hp=1325.945 |
| 40 | refine | 7/7 | 7.8263 | yes | session.rest_heal_ratio*1.222 (refine) |
| 41 | refine | 7/7 | 7.8263 | yes | drops.potion_chance*1.079 (refine) |
| 42 | refine | 7/7 | 7.8263 | yes | session.rest_heal_ratio*0.780 (refine) |
| 43 | refine | 7/7 | 7.8263 | yes | monsters.BossBalrog.attack*0.943 (refine) |
| 44 | refine | 6/7 | 6.8265 | no | risk.attack_scale_at_full_risk*1.197 (refine) |
| 45 | kick | 7/7 | 7.8246 | no | kick[1]: drops.potion_chance=0.5, player.attack_per_level=1.912, player.max_health=124.707 |
| 46 | kick | 6/7 | 6.9097 | no | kick[1]: player.potion_heal=76.598, session.wave_duration_per_wave=1.961, risk.attack_scale_at_full_risk=1.243 |
| 47 | kick | 7/7 | 7.8427 | yes | kick[1]: session.wave_duration_per_wave=3.486, monsters.BossBalrog.attack=15.502, player.base_attack=20.896 |
| 48 | refine | 7/7 | 7.8463 | yes | session.wave_duration_per_wave*0.980 (refine) |
| 49 | refine | 7/7 | 7.8463 | yes | drops.food_chance*0.911 (refine) |
| 50 | refine | 7/7 | 7.8288 | no | session.wave_duration_per_wave*1.128 (refine) |
| 51 | refine | 7/7 | 7.8463 | yes | drops.food_chance*0.911 (refine) |
| 52 | refine | 7/7 | 7.8494 | yes | player.max_health*1.097 (refine) |
| 53 | refine | 7/7 | 7.8474 | no | monsters.BossBalrog.hp*1.115 (refine) |
| 54 | refine | 6/7 | 6.8472 | no | player.base_attack*0.916 (refine) |
| 55 | refine | 7/7 | 7.8707 | yes | session.wave_duration_per_wave*0.861 (refine) |
| 56 | refine | 6/7 | 6.8727 | no | monsters.BossBalrog.hp*0.920 (refine) |
| 57 | refine | 7/7 | 7.8707 | yes | drops.potion_chance*1.132 (refine) |
| 58 | refine | 7/7 | 7.879 | yes | session.wave_duration_per_wave*0.905 (refine) |
| 59 | refine | 7/7 | 7.912 | yes | session.base_wave_duration*0.915 (refine) |
| 60 | refine | 7/7 | 7.912 | yes | drops.food_chance*0.948 (refine) |
| 61 | refine | 7/7 | 7.9136 | yes | risk.attack_scale_at_full_risk*0.927 (refine) |
| 62 | refine | 7/7 | 7.906 | no | session.wave_duration_per_wave*1.076 (refine) |
| 63 | refine | 7/7 | 7.9136 | yes | drops.food_chance*1.180 (refine) |
| 64 | refine | 7/7 | 7.9126 | no | monsters.BossBalrog.hp*1.053 (refine) |
| 65 | refine | 7/7 | 7.9198 | yes | session.base_wave_duration*0.990 (refine) |
| 66 | refine | 7/7 | 7.9188 | no | monsters.EliteGolem.attack*1.136 (refine) |
| 67 | refine | 7/7 | 7.9178 | no | monsters.BossBalrog.hp*1.089 (refine) |
| 68 | refine | 7/7 | 7.9174 | no | player.max_health*0.980 (refine) |
| 69 | refine | 7/7 | 7.9186 | no | player.max_health*0.921 (refine) |
| 70 | refine | 7/7 | 7.9208 | yes | monsters.BossBalrog.hp*0.970 (refine) |
| 71 | refine | 6/7 | 6.9188 | no | player.base_attack*0.896 (refine) |
| 72 | refine | 7/7 | 7.9205 | no | player.base_attack*0.986 (refine) |
| 73 | refine | 7/7 | 7.9218 | yes | session.rest_heal_ratio*0.920 (refine) |
| 74 | refine | 7/7 | 7.9505 | yes | session.base_wave_duration*0.905 (refine) |
| 75 | refine | 7/7 | 7.9445 | no | risk.attack_scale_at_full_risk*0.861 (refine) |
| 76 | refine | 7/7 | 7.9505 | yes | session.rest_heal_ratio*1.224 (refine) |
| 77 | refine | 7/7 | 7.9498 | no | risk.attack_scale_at_full_risk*0.810 (refine) |
| 78 | refine | 7/7 | 7.9504 | no | player.base_attack*1.027 (refine) |
| 79 | refine | 7/7 | 7.9447 | no | session.wave_duration_per_wave*1.054 (refine) |
| 80 | kick | 7/7 | 7.9534 | yes | kick[1]: player.potion_heal=89.095, risk.attack_scale_at_full_risk=0.709, monsters.EliteGolem.attack=9.3 |
