-- MonsterCollection
-- MapleStory Worlds Logic: monster discovery collection (도감) with permanent passive bonuses.
-- First defeat of each monster type registers a collection entry; each entry grants
-- +attack% and +max health per BalanceTable.CollectionAttackBonus / CollectionHealthBonus.

Property:
    [Sync]
    string DiscoveredCsv = ""
    [Sync]
    integer EntryCount = 0
    [Sync]
    number AttackBonusPercent = 0.0
    [Sync]
    number HealthBonusFlat = 0.0
    [None]
    number AttackBonusPerEntry = 0.03
    [None]
    number HealthBonusPerEntry = 6.0

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.DiscoveredCsv = ""
        self.EntryCount = 0
        self.AttackBonusPercent = 0.0
        self.HealthBonusFlat = 0.0
        log("[MapleSurvivalExpedition] Monster collection initialized")
    }

    [Server Only]
    void RegisterDiscovery(string monsterName)
    {
        if self:IsDiscovered(monsterName) then
            return
        end

        if self.DiscoveredCsv == "" then
            self.DiscoveredCsv = monsterName
        else
            self.DiscoveredCsv = self.DiscoveredCsv .. "," .. monsterName
        end

        self.EntryCount = self.EntryCount + 1
        self.AttackBonusPercent = self.EntryCount * self.AttackBonusPerEntry
        self.HealthBonusFlat = self.EntryCount * self.HealthBonusPerEntry
        log("[MapleSurvivalExpedition] Collection entry added: " .. monsterName .. " (total " .. tostring(self.EntryCount) .. ")")
    }

    [Server Only]
    boolean IsDiscovered(string monsterName)
    {
        if self.DiscoveredCsv == "" then
            return false
        end
        for entry in string.gmatch(self.DiscoveredCsv, "[^,]+") do
            if entry == monsterName then
                return true
            end
        end
        return false
    }

    [Server Only]
    number GetAttackMultiplier()
    {
        return 1.0 + self.AttackBonusPercent
    }

    [Server Only]
    number GetHealthBonus()
    {
        return self.HealthBonusFlat
    }
