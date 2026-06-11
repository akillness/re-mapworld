-- MonsterSpawner
-- MapleStory Worlds Component: wave-aware monster spawn point.
-- Attach to an empty Entity in the map. Set MonsterModelId to a model Entry ID.

Property:
    [Sync]
    number SpawnInterval = 5.0
    [Sync]
    number Timer = 0.0
    [Sync]
    integer MaxMonsters = 10
    [Sync]
    integer CurrentMonsters = 0
    [Sync]
    integer TotalSpawned = 0
    [Sync]
    integer CurrentWave = 1
    [Sync]
    boolean Enabled = true
    [Sync]
    string MonsterModelId = ""
    [Sync]
    string SpawnParentPath = "/maps/map01"

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.Timer = 0.0
        self.CurrentMonsters = 0
        self.TotalSpawned = 0
        self.Enabled = true
        log("[MapleSurvivalExpedition] Monster spawner initialized")
    }

    [Server Only]
    void OnUpdate(number delta)
    {
        if not self.Enabled then
            return
        end

        if self.CurrentMonsters >= self:GetWaveCap() then
            return
        end

        self.Timer = self.Timer + delta
        if self.Timer >= self:GetWaveInterval() then
            self.Timer = 0.0
            self:SpawnMonster()
        end
    }

    [Server Only]
    integer GetWaveCap()
    {
        local cap = self.MaxMonsters + self.CurrentWave
        if cap > 40 then
            cap = 40
        end
        return cap
    }

    [Server Only]
    number GetWaveInterval()
    {
        local interval = self.SpawnInterval - (self.CurrentWave * 0.15)
        if interval < 1.25 then
            interval = 1.25
        end
        return interval
    }

    [Server Only]
    void SetWave(integer wave)
    {
        self.CurrentWave = wave
        if self.CurrentWave < 1 then
            self.CurrentWave = 1
        end
    }

    [Server Only]
    void SpawnMonster()
    {
        local spawnPos = self.Entity.TransformComponent.WorldPosition
        local parent = self.Entity.Parent

        if self.SpawnParentPath ~= "" then
            local configuredParent = _EntityService:GetEntityByPath(self.SpawnParentPath)
            if isvalid(configuredParent) then
                parent = configuredParent
            end
        end

        if self.MonsterModelId == "" then
            self.CurrentMonsters = self.CurrentMonsters + 1
            self.TotalSpawned = self.TotalSpawned + 1
            log("[MapleSurvivalExpedition] Simulated monster spawn. Configure MonsterModelId for real spawned entities.")
            return
        end

        local monsterName = "ExpeditionMonster_W" .. tostring(self.CurrentWave) .. "_" .. tostring(self.TotalSpawned + 1)
        local spawnedEntity = _SpawnService:SpawnByModelId(self.MonsterModelId, monsterName, spawnPos, parent, "", true, true, true)

        if isvalid(spawnedEntity) then
            self.CurrentMonsters = self.CurrentMonsters + 1
            self.TotalSpawned = self.TotalSpawned + 1
            log("[MapleSurvivalExpedition] Spawned " .. monsterName .. ". Alive=" .. tostring(self.CurrentMonsters))
        else
            log("[MapleSurvivalExpedition] Spawn failed. Check MonsterModelId and parent path.")
        end
    }

    [Server Only]
    void OnMonsterDefeated()
    {
        self.CurrentMonsters = self.CurrentMonsters - 1
        if self.CurrentMonsters < 0 then
            self.CurrentMonsters = 0
        end
    }

    [Server Only]
    void ClearWaveCount()
    {
        self.CurrentMonsters = 0
        self.Timer = 0.0
    }
