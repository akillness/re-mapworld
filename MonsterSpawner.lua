-- MonsterSpawner
-- MapleStory Worlds Component: wave-scaled monster spawning with per-wave pools,
-- elite injection at high risk, and boss spawn on the boss wave.
-- Attach to a spawn-point entity under /maps/map01. Set MonsterModelId from
-- Resource Storage; leave empty for log-only simulated spawns.

Property:
    [Sync]
    string MonsterModelId = ""
    [Sync]
    number SpawnTimer = 0.0
    [Sync]
    integer CurrentMonsters = 0
    [Sync]
    integer TotalSpawned = 0
    [Sync]
    boolean BossSpawned = false
    [Sync]
    boolean EliteSpawnedThisWave = false
    [Sync]
    integer LastWave = 0
    [None]
    string WavePoolCsv = "Snail"
    [None]
    number SpawnInterval = 4.0
    [None]
    integer MaxAlive = 8

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.CurrentMonsters = 0
        self.TotalSpawned = 0
        self.BossSpawned = false
        log("[MapleSurvivalExpedition] Monster spawner ready")
    }

    [Server Only]
    void OnUpdate(number delta)
    {
        local manager = _EntityService:GetEntityByPath("/maps/map01/SurvivalGameManager").SurvivalGameManager
        if manager.IsComplete or manager.IsWaveActive == false then
            return
        end

        if manager.CurrentWave ~= self.LastWave then
            self.LastWave = manager.CurrentWave
            self.EliteSpawnedThisWave = false
        end

        self:RefreshWaveConfig(manager.CurrentWave)

        if manager.CurrentWaveType == "boss" and self.BossSpawned == false then
            self:SpawnMonster("BossBalrog", manager.RiskPercent)
            self.BossSpawned = true
            return
        end

        if self.CurrentMonsters >= self.MaxAlive then
            return
        end

        self.SpawnTimer = self.SpawnTimer + delta
        if self.SpawnTimer >= self.SpawnInterval then
            self.SpawnTimer = 0.0
            self:SpawnMonster(self:PickFromPool(), manager.RiskPercent)

            if manager.CurrentWaveType == "elite" and manager.RiskPercent > 50.0 and self.EliteSpawnedThisWave == false then
                self:SpawnMonster("EliteGolem", manager.RiskPercent)
                self.EliteSpawnedThisWave = true
            end
        end
    }

    [Server Only]
    void RefreshWaveConfig(integer wave)
    {
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        local waveType, spawnInterval, maxAlive = balance:GetWaveConfig(wave)
        self.SpawnInterval = spawnInterval
        self.MaxAlive = maxAlive
        self.WavePoolCsv = self:GetWavePool(wave)
    }

    [Server Only]
    string GetWavePool(integer wave)
    {
        if wave <= 1 then return "Snail" end
        if wave == 2 then return "Snail,Mushroom" end
        if wave == 3 then return "Mushroom,Slime" end
        if wave <= 5 then return "Slime,Stump" end
        if wave <= 7 then return "Stump,WildBoar" end
        return "WildBoar"
    }

    [Server Only]
    string PickFromPool()
    {
        local entries = {}
        for entry in string.gmatch(self.WavePoolCsv, "[^,]+") do
            table.insert(entries, entry)
        end
        local index = _UtilLogic:RandomIntegerRange(1, #entries)
        return entries[index]
    }

    [Server Only]
    void SpawnMonster(string monsterName, number riskPercent)
    {
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        local hp, attack, exp = balance:GetMonsterStats(monsterName)
        local hpScaled = hp * (1.0 + (riskPercent / 100.0) * balance.RiskHpScale)

        self.CurrentMonsters = self.CurrentMonsters + 1
        self.TotalSpawned = self.TotalSpawned + 1

        if self.MonsterModelId == "" then
            log("[MapleSurvivalExpedition] (simulated) spawn " .. monsterName .. " hp=" .. tostring(hpScaled))
            return
        end

        local spawned = _SpawnService:SpawnByModelId(self.MonsterModelId, monsterName, self.Entity.TransformComponent.Position, self.Entity.Parent)
        local agent = spawned.MonsterAgent
        agent.MonsterName = monsterName
        agent.Health = hpScaled
        agent.AttackDamage = attack
        agent.ExpReward = exp
        agent.SpawnerEntityPath = self.Entity.Path
        log("[MapleSurvivalExpedition] spawn " .. monsterName .. " hp=" .. tostring(hpScaled))
    }

    [Server Only]
    void NotifyMonsterDefeated()
    {
        if self.CurrentMonsters > 0 then
            self.CurrentMonsters = self.CurrentMonsters - 1
        end
    }
