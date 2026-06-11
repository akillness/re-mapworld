-- MonsterAgent
-- MapleStory Worlds Component: typed monster combat agent with risk-scaled attacks,
-- consumable drops, collection registration, and boss-defeat notification.
-- Attach to the monster model prefab used by MonsterSpawner.

Property:
    [Sync]
    string MonsterName = "Snail"
    [Sync]
    number Health = 30
    [Sync]
    number AttackDamage = 3
    [Sync]
    integer ExpReward = 20
    [Sync]
    number AttackInterval = 1.0
    [Sync]
    number AttackTimer = 0.0
    [None]
    string SpawnerEntityPath = ""

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.AttackTimer = 0.0
    }

    [Server Only]
    void OnUpdate(number delta)
    {
        if self.Health <= 0 then
            return
        end

        self.AttackTimer = self.AttackTimer + delta
        if self.AttackTimer < self.AttackInterval then
            return
        end
        self.AttackTimer = 0.0

        local manager = _EntityService:GetEntityByPath("/maps/map01/SurvivalGameManager").SurvivalGameManager
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        local riskScale = 1.0 + (manager.RiskPercent / 100.0) * balance.RiskAttackScale

        local player = _UserService.LocalPlayer
        if player == nil then
            return
        end
        local stats = player.PlayerSurvivalStats
        stats:ApplyDamage(self.AttackDamage * riskScale)
    }

    [Server Only]
    void TakeDamage(number amount)
    {
        if self.Health <= 0 then
            return
        end

        self.Health = self.Health - amount
        if self.Health <= 0 then
            self:OnDefeated()
        end
    }

    [Server Only]
    void OnDefeated()
    {
        local player = _UserService.LocalPlayer
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        local collection = _EntityService:GetEntityByPath("/maps/map01/MonsterCollection").MonsterCollection
        local manager = _EntityService:GetEntityByPath("/maps/map01/SurvivalGameManager").SurvivalGameManager

        if player ~= nil then
            local stats = player.PlayerSurvivalStats
            stats:GainExp(self.ExpReward)

            local potionDrop = 0
            local foodDrop = 0
            if _UtilLogic:RandomDouble() < balance.PotionDropChance then
                potionDrop = 1
            end
            if _UtilLogic:RandomDouble() < balance.FoodDropChance then
                foodDrop = 1
            end
            stats:AddDrop(potionDrop, foodDrop)
        end

        collection:RegisterDiscovery(self.MonsterName)

        if self.MonsterName == "BossBalrog" then
            manager:NotifyBossDefeated()
        end

        if self.SpawnerEntityPath ~= "" then
            local spawnerEntity = _EntityService:GetEntityByPath(self.SpawnerEntityPath)
            if spawnerEntity ~= nil then
                spawnerEntity.MonsterSpawner:NotifyMonsterDefeated()
            end
        end

        log("[MapleSurvivalExpedition] " .. self.MonsterName .. " defeated. Exp=" .. tostring(self.ExpReward))
        self.Entity:Destroy()
    }
