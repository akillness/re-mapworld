-- BattleSystem: HP/MP 및 피해 로직 (Maple Soul Hero 참고)
local BattleSystem = {}

function BattleSystem:ApplyDamage(attacker, victim, damage)
    victim.HP = math.max(0, victim.HP - damage)
    if victim.HP == 0 then
        self:OnEntityDeath(victim)
    end
end

function BattleSystem:OnEntityDeath(entity)
    if entity.Type == "Boss" then
        print("Boss Defeated! Extraction Portal opens for 30s.")
        -- TODO: Portal spawn logic
    end
end

return BattleSystem
