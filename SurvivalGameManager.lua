-- SurvivalGameManager
-- MapleStory Worlds Logic: expedition wave pacing, wave types (normal/elite/boss),
-- risk gauge, escape decision window, scoring, and session settlement.
-- Balance values come from the BalanceTable logic (generated from balance_table.json).

Property:
    [Sync]
    integer CurrentWave = 1
    [Sync]
    number WaveTimer = 0.0
    [Sync]
    number RestTimer = 0.0
    [Sync]
    number RiskPercent = 0.0
    [Sync]
    integer TargetWave = 10
    [Sync]
    string CurrentWaveType = "normal"
    [Sync]
    boolean IsWaveActive = false
    [Sync]
    boolean IsRestPhase = false
    [Sync]
    boolean EscapeWindowOpen = false
    [Sync]
    boolean IsComplete = false
    [Sync]
    boolean BossDefeated = false
    [Sync]
    string SessionOutcome = "running"
    [Sync]
    integer AccountExp = 0
    [None]
    number AccountExpPerScore = 0.1
    [None]
    number WipeKeepRatio = 0.4

Method:
    [Server Only]
    void OnBeginPlay()
    {
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        self.TargetWave = balance.TargetWave
        self.CurrentWave = 1
        self.IsComplete = false
        self.BossDefeated = false
        self.SessionOutcome = "running"
        self:StartWave()
    }

    [Server Only]
    void OnUpdate(number delta)
    {
        if self.IsComplete then
            return
        end

        if self.IsWaveActive then
            self.WaveTimer = self.WaveTimer - delta
            self.RiskPercent = 100.0 - ((self.WaveTimer / self:GetWaveDuration()) * 100.0)
            if self.RiskPercent < 0 then
                self.RiskPercent = 0
            end
            if self.RiskPercent > 100 then
                self.RiskPercent = 100
            end

            if self.CurrentWaveType == "boss" then
                if self.BossDefeated then
                    self:EndWave()
                end
            elseif self.WaveTimer <= 0 then
                self:EndWave()
            end
        elseif self.IsRestPhase then
            self.RestTimer = self.RestTimer - delta
            if self.RestTimer <= 0 then
                self.EscapeWindowOpen = false
                self.IsRestPhase = false
                self.CurrentWave = self.CurrentWave + 1
                self:StartWave()
            end
        end
    }

    [Server Only]
    number GetWaveDuration()
    {
        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        return balance:GetWaveDuration(self.CurrentWave)
    }

    [Server Only]
    void StartWave()
    {
        if self.CurrentWave > self.TargetWave then
            self:CompleteExpedition("cleared")
            return
        end

        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        local waveType, spawnInterval, maxAlive = balance:GetWaveConfig(self.CurrentWave)
        self.CurrentWaveType = waveType
        self.IsWaveActive = true
        self.IsRestPhase = false
        self.RiskPercent = 0.0
        self.WaveTimer = self:GetWaveDuration()
        log("[MapleSurvivalExpedition] Wave " .. tostring(self.CurrentWave) .. " (" .. waveType .. ") started. Duration=" .. tostring(self.WaveTimer))
    }

    [Server Only]
    void EndWave()
    {
        self.IsWaveActive = false
        self.RiskPercent = 100.0

        if self.CurrentWave >= self.TargetWave then
            self:CompleteExpedition("cleared")
            return
        end

        local balance = _EntityService:GetEntityByPath("/maps/map01/BalanceTable").BalanceTable
        self.IsRestPhase = true
        self.EscapeWindowOpen = true
        self.RestTimer = balance.RestDuration
        log("[MapleSurvivalExpedition] Wave " .. tostring(self.CurrentWave) .. " cleared. Escape window open for " .. tostring(self.RestTimer) .. "s")
    }

    [Server Only]
    void NotifyBossDefeated()
    {
        self.BossDefeated = true
        log("[MapleSurvivalExpedition] Boss defeated!")
    }

    [Server Only]
    void RequestEscape(integer playerScore)
    {
        if self.EscapeWindowOpen == false then
            return
        end
        self:Settle(playerScore, 1.0)
        self:CompleteExpedition("escaped")
    }

    [Server Only]
    void NotifyPlayerWiped(integer playerScore)
    {
        self:Settle(playerScore, self.WipeKeepRatio)
        self:CompleteExpedition("wiped")
    }

    [Server Only]
    void Settle(integer playerScore, number keepRatio)
    {
        self.AccountExp = self.AccountExp + math.floor(playerScore * keepRatio * self.AccountExpPerScore)
        log("[MapleSurvivalExpedition] Settlement: score=" .. tostring(playerScore) .. " accountExp=" .. tostring(self.AccountExp))
    }

    [Server Only]
    void CompleteExpedition(string outcome)
    {
        self.IsComplete = true
        self.IsWaveActive = false
        self.IsRestPhase = false
        self.EscapeWindowOpen = false
        self.RiskPercent = 100.0
        self.SessionOutcome = outcome
        log("[MapleSurvivalExpedition] Expedition finished. Outcome=" .. outcome)
    }
