-- MonsterAgent
-- MapleStory Worlds Component: simple server-side monster stat and reward logic.
-- Attach this to the monster model used by MonsterSpawner.

Property:
    [Sync]
    number Health = 30
    [Sync]
    number MaxHealth = 30
    [Sync]
    number AttackDamage = 8
    [Sync]
    number AttackInterval = 1.5
    [Sync]
    number AttackTimer = 0.0
    [Sync]
    integer ExpReward = 25
    [Sync]
    boolean IsDead = false

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.Health = self.MaxHealth
        self.AttackTimer = 0.0
        self.IsDead = false
        log("[MapleSurvivalExpedition] Monster ready: " .. self.Entity.Name)
    }

    [Server Only]
    void OnUpdate(number delta)
    {
        if self.IsDead then
            return
        end

        self.AttackTimer = self.AttackTimer + delta
        if self.AttackTimer >= self.AttackInterval then
            self.AttackTimer = 0.0
            log("[MapleSurvivalExpedition] Monster attack tick: " .. self.Entity.Name)
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
    void Die()
    {
        self.IsDead = true
        log("[MapleSurvivalExpedition] Monster defeated: " .. self.Entity.Name .. ", exp=" .. tostring(self.ExpReward))
        _EntityService:Destroy(self.Entity)
    }
