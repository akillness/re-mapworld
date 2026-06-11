-- BalanceTable
-- MapleStory Worlds Logic: generated from balance_table.json by tools/msw_project_cli.py gen-lua.
-- Data-driven balance per docs/join_develop.md. Do not edit by hand; edit balance_table.json.

Property:
    [Sync]
    integer TargetWave = 10
    [Sync]
    number BaseWaveDuration = 37.0647
    [Sync]
    number WaveDurationPerWave = 2.6599
    [Sync]
    number RestDuration = 8.0
    [Sync]
    number RestHealRatio = 0.0815
    [Sync]
    number PlayerMaxHealth = 102.9937
    [Sync]
    number PlayerBaseAttack = 20.8959
    [Sync]
    number PlayerAttackPerLevel = 2.3328
    [Sync]
    number PotionHeal = 89.0953
    [Sync]
    number FoodRestore = 30.0
    [Sync]
    number RiskAttackScale = 0.7092
    [Sync]
    number RiskHpScale = 0.25
    [Sync]
    number PotionDropChance = 0.5
    [Sync]
    number FoodDropChance = 0.3839
    [Sync]
    number CollectionAttackBonus = 0.03
    [Sync]
    number CollectionHealthBonus = 6.0

Method:
    [Server Only]
    void OnBeginPlay()
    {
        log("[MapleSurvivalExpedition] BalanceTable loaded. TargetWave=" .. tostring(self.TargetWave))
    }

    [Server Only]
    number GetWaveDuration(integer wave)
    {
        return self.BaseWaveDuration + (wave * self.WaveDurationPerWave)
    }

    [Server Only]
    string GetWaveType(integer wave)
    {
        local waveType, interval, maxAlive = self:GetWaveConfig(wave)
        return waveType
    }

    [Server Only]
    string,number,integer GetWaveConfig(integer wave)
    {
        if wave == 1 then return "normal", 4.5, 6 end
        if wave == 2 then return "normal", 4.2, 7 end
        if wave == 3 then return "elite", 4.0, 8 end
        if wave == 4 then return "normal", 3.8, 9 end
        if wave == 5 then return "normal", 3.6, 10 end
        if wave == 6 then return "elite", 3.4, 11 end
        if wave == 7 then return "normal", 3.2, 12 end
        if wave == 8 then return "normal", 3.0, 13 end
        if wave == 9 then return "elite", 2.8, 14 end
        if wave == 10 then return "boss", 3.5, 6 end
        return "normal", 4.0, 8
    }

    [Server Only]
    number,number,integer GetMonsterStats(string monsterName)
    {
        if monsterName == "Snail" then return 28, 2.2, 18 end
        if monsterName == "Mushroom" then return 42, 3.2, 26 end
        if monsterName == "Slime" then return 58, 4.2, 34 end
        if monsterName == "Stump" then return 80, 5.5, 46 end
        if monsterName == "WildBoar" then return 105, 7.0, 60 end
        if monsterName == "EliteGolem" then return 240, 9.2995, 140 end
        if monsterName == "BossBalrog" then return 1286.343, 15.5017, 600 end
        return 30, 3, 20
    }
