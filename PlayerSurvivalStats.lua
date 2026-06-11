-- PlayerSurvivalStats
-- MapleStory Worlds Component: player survival, leveling, and death/respawn state.

Property:
    [Sync]
    number Health = 100
    [Sync]
    number MaxHealth = 100
    [Sync]
    number Hunger = 100
    [Sync]
    number MaxHunger = 100
    [Sync]
    number HungerDrainPerSecond = 0.45
    [Sync]
    number StarvationDamagePerSecond = 2.5
    [Sync]
    integer Level = 1
    [Sync]
    integer Exp = 0
    [Sync]
    integer Score = 0
    [Sync]
    boolean IsDead = false

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.Health = self.MaxHealth
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

        self.Hunger = self.Hunger - (delta * self.HungerDrainPerSecond)
        if self.Hunger < 0 then
            self.Hunger = 0
        end

        if self.Hunger <= 0 then
            self:ApplyDamage(delta * self.StarvationDamagePerSecond)
        end
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
        if self.Health > self.MaxHealth then
            self.Health = self.MaxHealth
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
            self.MaxHealth = self.MaxHealth + 20
            self.Health = self.MaxHealth
            self.MaxHunger = self.MaxHunger + 5
            self.Hunger = self.MaxHunger
            log("[MapleSurvivalExpedition] Level up! Level=" .. tostring(self.Level))
        end
    }

    [Server Only]
    void Die()
    {
        self.IsDead = true
        log("[MapleSurvivalExpedition] Player died. Resetting survival state for test loop.")
        self.Health = self.MaxHealth
        self.Hunger = self.MaxHunger
        self.IsDead = false
    }
