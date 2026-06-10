-- SurvivalManager: 위험도 및 세션 관리
local SurvivalManager = {}

SurvivalManager.DangerGauge = 0
SurvivalManager.IsSafeZone = false
SurvivalManager.BossSpawned = false

function SurvivalManager:UpdateDanger(deltaTime)
    if not self.IsSafeZone then
        self.DangerGauge = self.DangerGauge + (0.1 * deltaTime) -- 10초당 1% (0.1% per sec)
        if self.DangerGauge >= 100 and not self.BossSpawned then
            self:SpawnBoss()
        end
    end
end

function SurvivalManager:SpawnBoss()
    self.BossSpawned = true
    print("CRITICAL: Dark Slime Boss has appeared!")
    -- TODO: Boss spawn logic via MSW API
end

function SurvivalManager:OnSafeZoneEnter()
    self.IsSafeZone = true
    print("Safe Zone: Danger gauge frozen. HP recovery active.")
end

function SurvivalManager:OnSafeZoneExit()
    self.IsSafeZone = false
end

return SurvivalManager
