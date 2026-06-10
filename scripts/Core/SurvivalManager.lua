-- SurvivalManager: 위험도 및 세션 관리 (추적 로그 강화)
local SurvivalManager = {}

SurvivalManager.DangerGauge = 0
SurvivalManager.IsSafeZone = false
SurvivalManager.BossSpawned = false

function SurvivalManager:UpdateDanger(deltaTime)
    if not self.IsSafeZone then
        self.DangerGauge = self.DangerGauge + (0.1 * deltaTime)
        -- 추적 로그: 엔진 툴 콘솔에서 확인 가능하도록 출력
        if math.floor(self.DangerGauge) % 10 == 0 then
            print("[TRACKING] Current Danger Gauge: " .. math.floor(self.DangerGauge) .. "%")
        end
        
        if self.DangerGauge >= 100 and not self.BossSpawned then
            self:SpawnBoss()
        end
    else
        -- 세이프 존 추적 로그
        print("[TRACKING] Player in SAFE ZONE. Gauge frozen.")
    end
end

function SurvivalManager:SpawnBoss()
    self.BossSpawned = true
    print("[TRACKING] CRITICAL: Dark Slime Boss has appeared!")
end

return SurvivalManager
