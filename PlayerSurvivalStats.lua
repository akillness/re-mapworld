-- PlayerSurvivalStats
-- MapleStory Worlds Component: player survival, combat power, consumables,
-- leveling, collection bonuses, and death/settlement state.
-- Balance values come from the BalanceTable logic (generated from balance_table.json).

Property:
    [Sync]
    number Health = 120
    [Sync]
    number MaxHealth = 120
    [Sync]
    number Hunger = 100
    [Sync]
    number MaxHunger = 100
    [Sync]
    number HungerDrainPerSecond = 0.4
    [Sync]
    number StarvationDamagePerSecond = 2.0
    [Sync]
    number BaseAttack = 9.0
    [Sync]
    number AttackPerLevel = 2.0
    [Sync]
    integer Level = 1
    [Sync]
    integer Exp = 0
    [Sync]
    integer Score = 0
    [Sync]
    integer Potions = 2
    [Sync]
    integer Food = 2
    [Sync]
    boolean IsDead = false
    [None]
    number PotionHeal = 45.0
    [None]
    number FoodRestore = 30.0
    [None]
    number PotionUseThreshold = 0.55
    [None]
    number FoodUseThreshold = 0.45

Method:
    [Server Only]
    void OnBeginPlay()
    {
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        self.MaxHealth = balance.PlayerMaxHealth
        self.BaseAttack = balance.PlayerBaseAttack
        self.AttackPerLevel = balance.PlayerAttackPerLevel
        self.PotionHeal = balance.PotionHeal
        self.FoodRestore = balance.FoodRestore
        self.Health = self:GetEffectiveMaxHealth()
        self.Hunger = self.MaxHunger
        self.Level = 1
        self.Exp = 0
        self.Score = 0
        self.IsDead = false
        log("[MapleSurvivalExpedition] Player survival stats initialized")
    }

    [Server Only]
    void OnUpdate(number delta)
    {
        if self.IsDead then
            return
        end

        local manager = _EntityService:GetEntityByPath("/maps/map01/SurvivalGameManager").SurvivalGameManager
        if manager.IsRestPhase then
            local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
            self:Heal(self:GetEffectiveMaxHealth() * balance.RestHealRatio * delta)
        end

        self.Hunger = self.Hunger - (delta * self.HungerDrainPerSecond)
        if self.Hunger < 0 then
            self.Hunger = 0
        end

        if self.Hunger <= 0 then
            self:ApplyDamage(delta * self.StarvationDamagePerSecond)
        end

        self:AutoConsume()
    }

    [Server Only]
    number GetAttackPower()
    {
        local collection = _EntityService:GetEntityByPath("/maps/map01/MonsterCollection").MonsterCollection
        local power = self.BaseAttack + ((self.Level - 1) * self.AttackPerLevel)
        return power * collection:GetAttackMultiplier()
    }

    [Server Only]
    number GetEffectiveMaxHealth()
    {
        local collection = _EntityService:GetEntityByPath("/maps/map01/MonsterCollection").MonsterCollection
        return self.MaxHealth + collection:GetHealthBonus()
    }

    [Server Only]
    void AutoConsume()
    {
        if self.Potions > 0 and self.Health < (self:GetEffectiveMaxHealth() * self.PotionUseThreshold) then
            self.Potions = self.Potions - 1
            self:Heal(self.PotionHeal)
            log("[MapleSurvivalExpedition] Potion used. Remaining=" .. tostring(self.Potions))
        end
        if self.Food > 0 and self.Hunger < (self.MaxHunger * self.FoodUseThreshold) then
            self.Food = self.Food - 1
            self:Eat(self.FoodRestore)
        end
    }

    [Server Only]
    void AddDrop(integer potions, integer food)
    {
        self.Potions = self.Potions + potions
        self.Food = self.Food + food
    }

    [Server Only]
    void ApplyDamage(number amount)
    {
        if self.IsDead then
            return
        end

        self.Health = self.Health - amount
        if self.Health <= 0 then
            self.Health = 0
            self:Die()
        end
    }

    [Server Only]
    void Heal(number amount)
    {
        if self.IsDead then
            return
        end

        self.Health = self.Health + amount
        local cap = self:GetEffectiveMaxHealth()
        if self.Health > cap then
            self.Health = cap
        end
    }

    [Server Only]
    void Eat(number amount)
    {
        if self.IsDead then
            return
        end

        self.Hunger = self.Hunger + amount
        if self.Hunger > self.MaxHunger then
            self.Hunger = self.MaxHunger
        end
        log("[MapleSurvivalExpedition] Food consumed. Hunger=" .. tostring(self.Hunger))
    }

    [Server Only]
    void GainExp(integer amount)
    {
        if self.IsDead then
            return
        end

        self.Exp = self.Exp + amount
        self.Score = self.Score + amount

        while self.Exp >= (self.Level * 100) do
            self.Exp = self.Exp - (self.Level * 100)
            self.Level = self.Level + 1
            self.MaxHealth = self.MaxHealth + 18
            self.Health = self:GetEffectiveMaxHealth()
            self.MaxHunger = self.MaxHunger + 5
            self.Hunger = self.MaxHunger
            log("[MapleSurvivalExpedition] Level up! Level=" .. tostring(self.Level))
        end
    }

    [Server Only]
    void Die()
    {
        self.IsDead = true
        local manager = _EntityService:GetEntityByPath("/maps/map01/SurvivalGameManager").SurvivalGameManager
        manager:NotifyPlayerWiped(self.Score)
        log("[MapleSurvivalExpedition] Player wiped. Partial settlement applied.")
    }
