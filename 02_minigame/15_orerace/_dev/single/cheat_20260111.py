import minescript as m

player = "@p"

# ==================================================
# エフェクト付与
# ==================================================
effects = [
    "night_vision infinite 0 true",        # 暗視
    "saturation infinite 0 true",           # 空腹にならない
    "resistance infinite 255 true",         # ほぼ無敵
    # "slow_falling infinite 0 true",         # 落下ダメージなし
    "water_breathing infinite 0 true",      # 水中呼吸
    "dolphins_grace infinite 0 true",       # 水中高速移動
    "speed infinite 2 true",                # 移動速度UP
    "haste infinite 2 true",                # 採掘速度UP
    "fire_resistance infinite 0 true",       # 炎耐性
    "health_boost infinite 4 true"
]

for effect in effects:
    m.execute(f"/effect give {player} minecraft:{effect}")

# ==================================================
# アイテム付与
# ==================================================
m.execute("/give @p minecraft:diamond_pickaxe 1")

# ==================================================
# ゲームルール・設定
# ==================================================

# 死亡時インベントリ保持
m.execute("/gamerule keepInventory true")

# ゲーム難易度をピースフル
m.execute("/difficulty peaceful")

# （任意）天候固定・時間固定したい場合
# m.execute("/weather clear 999999")
# m.execute("/gamerule doDaylightCycle false")

# m.execute("/gamerule doMobSpawning false")
# m.execute("/gamerule mobGriefing false")
# m.execute("/gamerule fireSpread false")
