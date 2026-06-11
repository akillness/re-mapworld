-- SurvivalGameManager
-- MapleStory Worlds Logic: expedition wave pacing, risk, scoring, and completion state.

Property:
    [Sync]
    integer CurrentWave = 1
    [Sync]
    number WaveTimer = 0.0
    [Sync]
    number RestTimer = 0.0
    [Sync]
    number BaseWaveDuration = 45.0
    [Sync]
    number RestDuration = 10.0
    [Sync]
    number RiskPercent = 0.0
    [Sync]
    integer TargetWave = 5
    [Sync]
    boolean IsWaveActive = false
    [Sync]
    boolean IsComplete = false

Method:
    [Server Only]
    void OnBeginPlay()
    {
        self.CurrentWave = 1
        self.IsComplete = false
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

            if self.WaveTimer <= 0 then
                self:EndWave()
            end
        else
            self.RestTimer = self.RestTimer - delta
            if self.RestTimer <= 0 then
                self.CurrentWave = self.CurrentWave + 1
                self:StartWave()
            end
        end
    }

    [Server Only]
    number GetWaveDuration()
    {
        return self.BaseWaveDuration + (self.CurrentWave * 10.0)
    }

    [Server Only]
    void StartWave()
    {
        if self.CurrentWave > self.TargetWave then
            self:CompleteExpedition()
            return
        end

        self.IsWaveActive = true
        self.RiskPercent = 0.0
        self.WaveTimer = self:GetWaveDuration()
        log("[MapleSurvivalExpedition] Wave " .. tostring(self.CurrentWave) .. " started. Duration=" .. tostring(self.WaveTimer))
    }

    [Server Only]
    void EndWave()
    {
        self.IsWaveActive = false
        self.RiskPercent = 100.0

        if self.CurrentWave >= self.TargetWave then
            self:CompleteExpedition()
            return
        end

        self.RestTimer = self.RestDuration
        log("[MapleSurvivalExpedition] Wave " .. tostring(self.CurrentWave) .. " cleared. Rest=" .. tostring(self.RestTimer))
    }

    [Server Only]
    void CompleteExpedition()
    {
        self.IsComplete = true
        self.IsWaveActive = false
        self.RiskPercent = 100.0
        log("[MapleSurvivalExpedition] Expedition complete. All target waves cleared.")
    }
