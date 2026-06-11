-- SurvivalHudBridge
-- MapleStory Worlds Component: exposes synchronized HUD-friendly fields.
-- Attach to a UI manager entity or keep as a simple Logic helper.

Property:
    [Sync]
    string StageText = "Wave 1"
    [Sync]
    string HealthText = "HP 100/100"
    [Sync]
    string HungerText = "Hunger 100/100"
    [Sync]
    string RiskText = "Risk 0%"
    [Sync]
    boolean VictoryVisible = false

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.VictoryVisible = false
        self:Refresh(1, 100, 100, 100, 100, 0, false)
    }

    [Server Only]
    void Refresh(integer wave, number health, number maxHealth, number hunger, number maxHunger, number risk, boolean complete)
    {
        self.StageText = "Wave " .. tostring(wave)
        self.HealthText = "HP " .. tostring(math.floor(health)) .. "/" .. tostring(math.floor(maxHealth))
        self.HungerText = "Hunger " .. tostring(math.floor(hunger)) .. "/" .. tostring(math.floor(maxHunger))
        self.RiskText = "Risk " .. tostring(math.floor(risk)) .. "%"
        self.VictoryVisible = complete
    }
