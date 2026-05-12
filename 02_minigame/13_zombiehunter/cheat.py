import minescript as m

# ==============================
# 武器・防具（全て最大エンチャント）
# ==============================
gear = [
    '/give @p minecraft:diamond_sword[minecraft:enchantments={sharpness:5,fire_aspect:2,looting:3}] 1',
    '/give @p minecraft:diamond_helmet[minecraft:enchantments={protection:4,respiration:3,aqua_affinity:1}] 1',
    '/give @p minecraft:diamond_chestplate[minecraft:enchantments={protection:4,thorns:3}] 1',
    '/give @p minecraft:diamond_leggings[minecraft:enchantments={protection:4}] 1',
    '/give @p minecraft:diamond_boots[minecraft:enchantments={protection:4,feather_falling:4}] 1'
]

for item in gear:
    m.execute(item)

# ==============================
# ステータス強化（ポーション効果）
# ==============================
effects = [
    ("strength", 4),
    ("regeneration", 4),
    ("resistance", 4),
    ("fire_resistance", 0),
    ("speed", 4),
    ("absorption", 4),
    ("health_boost", 4)
]

for eff, lvl in effects:
    m.execute(f'/effect give @p minecraft:{eff} 1000000 {lvl} true')

# ==============================
# 完了メッセージ
# ==============================
m.echo("✅ プレイヤーを最強化しました！")
